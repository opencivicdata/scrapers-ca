from __future__ import unicode_literals
from utils import CanadianScraper

from pupa.scrape import Bill, Event
from urllib.parse import parse_qs, urlparse
import lxml.html
import datetime as dt
import pytz
import re

CALENDAR_DAY_TEMPLATE = 'http://app.toronto.ca/tmmis/meetingCalendarView.do?function=calendarCellView&year={}&month={}&date={}'
AGENDA_FULL_STANDARD_TEMPLATE = 'http://app.toronto.ca/tmmis/viewPublishedReport.do?function=getAgendaReport&meetingId={}'
AGENDA_LIST_STANDARD_TEMPLATE = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getAgendaItems&print=N&meetingId={}'
AGENDA_FULL_COUNCIL_TEMPLATE = 'http://app.toronto.ca/tmmis/viewPublishedReport.do?function=getCouncilAgendaReport&meetingId={}'
AGENDA_LIST_COUNCIL_TEMPLATE = 'http://app.toronto.ca/tmmis/viewAgendaItemList.do?function=getCouncilAgendaItems&print=N&meetingId={}'
AGENDA_ITEM_TEMPLATE = 'http://app.toronto.ca/tmmis/viewAgendaItemHistory.do?item={}'
COMMITTEE_LIST_TEMPLATE = 'http://app.toronto.ca/tmmis/decisionBodyList.do?function=displayDecisionBodyList&term={}'

STATUS_DICT = {
        'Scheduled': 'confirmed',
        'Scheduled (Preview)': 'confirmed',
        'Complete': 'passed',
        'Cancelled': 'cancelled',
        'No Quorum': 'cancelled',
        }

class TorontoIncrementalEventScraper(CanadianScraper):

    def __init__(self, jurisdiction, datadir, strict_validation=True, fastmode=False):
        super(TorontoIncrementalEventScraper, self).__init__(jurisdiction, datadir, strict_validation=True, fastmode=False)
        # Used to store mappings of committee names to two-letter codes
        self.committee_codes_d = {}

    def scrape(self):
        today = dt.datetime.today()
        delta_days = 7
        start_date = today - dt.timedelta(days=delta_days)
        end_date = today + dt.timedelta(days=delta_days*2)

        self.scrape_committee_codes()
        yield from self.scrape_events_range(start_date, end_date)

    def scrape_committee_codes(self):
        self.committee_codes_d = self.committee_codes()

    def parse_table(self, table_node):
        items = []

        def sanitize_key(str): return str.lower().strip().replace(' ', '_').replace('.', '')

        def sanitize_org_name(str):
            # Council committee name customized in ca_on_toronto
            org_name = 'Toronto City Council' if str == 'City Council' else str
            # Some meetings preceded with legend, ie "S:" for special meetings.
            org_name = re.sub(r'^[A-Z]: +', '', org_name)
            return org_name

        rows = table_node.xpath('tr')
        headers = [sanitize_key(col.text) for col in rows.pop(0)]
        for row in rows:
            meeting_link = row.cssselect('a')[0].attrib['href']
            values = [col.text_content().strip() for col in row]
            item = dict(zip(headers, values))
            item.update({'meeting': sanitize_org_name(item['meeting']) })
            item.update({'meeting_link': meeting_link})
            items.append(item)

        return items

    def extract_events_by_day(self, date):
        url = CALENDAR_DAY_TEMPLATE.format(date.year, date.month-1, date.day)
        page = self.lxmlize(url)

        tables = page.xpath('//table')
        if not tables:
            return []

        table_node = tables[0]

        raw_table_data = self.parse_table(table_node)

        def create_event_dict(row):
            event_dict = row

            link = row['meeting_link']
            meeting_id = parse_qs(urlparse(link).query)['meetingId'][0]
            event_dict.update({'meeting_id': meeting_id})


            return event_dict

        events = [create_event_dict(row) for row in raw_table_data]

        return events


    def scrape_events_range(self, start_date, end_date):

        def daterange(start_date, end_date):
            number_of_days = int((end_date - start_date).days)
            for n in range(number_of_days):
                yield start_date + dt.timedelta(n)

        for date in daterange(start_date, end_date):
            events = self.extract_events_by_day(date)
            for event in events:
                tz = pytz.timezone("America/Toronto")
                time = dt.datetime.strptime(event['time'], '%I:%M %p')
                start = tz.localize(date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0))
                source_url = CALENDAR_DAY_TEMPLATE.format(start.year, start.month, start.day)
                org_name = event['meeting']
                e = Event(
                    name = org_name,
                    start_time = start,
                    timezone = tz.zone,
                    location_name = event['location'],
                    status=STATUS_DICT[event['meeting_status']],
                    )
                e.add_source(source_url)
                e.extras = {
                    'meeting_number': event['no'],
                    'tmmis_meeting_id': event['meeting_id'],
                    }
                e.add_participant(
                    name = org_name,
                    type = 'organization',
                    )

                def is_agenda_available(event):
                    return event['publishing_status'] in ['Agenda Published', 'Minutes Published']

                def is_council(event):
                    return True if event['meeting'] == 'Toronto City Council' else False

                if is_agenda_available(event):
                    template = AGENDA_FULL_COUNCIL_TEMPLATE if is_council(event) else AGENDA_FULL_STANDARD_TEMPLATE
                    agenda_url = template.format(event['meeting_id'])
                    full_identifiers = list(self.full_identifiers(event['meeting_id'], is_council(event)))

                    e.add_source(agenda_url)
                    agenda_items = self.agenda_from_url(agenda_url)
                    for i, item in enumerate(agenda_items):

                        a = e.add_agenda_item(item['title'])
                        a['order'] = str(i)

                        def is_vote_event(item):
                            return True if item['type'] == 'ACTION' else False

                        def normalize_wards(raw):
                            if not raw: raw = 'All'
                            if raw == 'All':
                                return raw.lower()
                            else:
                                return raw.split(', ')

                        def is_being_introduced(item, event):
                            org_name = event['meeting']
                            identifier = item['identifier']

                            # `org_code` is two-letter code for committee
                            current_org_code = self.committee_codes_d.get(org_name)
                            originating_org_code = re.search(r'([A-Z]{2})[0-9]+\.[0-9]+', identifier).group(1)

                            return current_org_code == originating_org_code

                        if is_vote_event(item):
                            wards = normalize_wards(item['wards'])
                            identifier_regex = re.compile(r'^[0-9]{4}\.([A-Z]{2}[0-9]+\.[0-9]+)$')
                            [full_identifier] = [id for id in full_identifiers if identifier_regex.match(id).group(1) == item['identifier']]
                            a.add_bill(full_identifier)
                            if is_being_introduced(item, event):
                                b = Bill(
                                    # TODO: Fix this hardcode
                                    legislative_session = '2014-2018',
                                    identifier = full_identifier,
                                    title = item['title'],
                                    )
                                b.add_source(agenda_url)
                                b.add_document_link(note='canonical', media_type='text/html', url=AGENDA_ITEM_TEMPLATE.format(full_identifier))
                                b.extras = {
                                    'wards': wards,
                                    }

                                yield b

                yield e

    def agenda_from_url(self, url):
        page = self.lxmlize(url)
        main = page.xpath('//table[1]/..')[0]
        top_level_elems = main.getchildren()
        section_breaks = page.cssselect('table.border')

        section_break_indices = [i for i, elem in enumerate(top_level_elems) if elem in section_breaks]

        def partition(alist, indices): return [alist[i:j] for i, j in zip([0]+indices, indices+[None])]

        sections = partition(top_level_elems, section_break_indices)

        def treeify_section_list(section):
            tree = lxml.html.Element('section')
            for elem in section:
                tree.append(elem)

            return tree

        section_trees = [treeify_section_list(section) for section in sections]

        preamble = section_trees.pop(0)
        agenda_items = section_trees

        items = []
        newline_regex = re.compile(r' ?\r\n ?')
        for item in agenda_items:
            dict = {
                    'identifier': item.xpath('//table[1]//td[1]')[0].text_content(),
                    'type': item.xpath('//table[1]//td[2]')[0].text_content().strip(),
                    'wards': item.xpath('//table[1]//td[5]')[0].text_content().strip().replace('Ward:',''),
                    'title': newline_regex.sub(' ', item.xpath('//table[2]//td[1]')[0].text_content().strip()),
                    }

            items.append(dict)

        return items

    def committee_codes(self):
        codes = {}
        terms = [
            '2014-2018',
            #'2010-2014', # Disabled for speed
            #'2006-2010', # Disabled for speed
            # TODO: Accommodate legacy format pages.
            #'2003-2006',
            #'2000-2003',
            #'1998-2000',
            ]
        for term in terms:
            page = self.lxmlize(COMMITTEE_LIST_TEMPLATE.format(term))
            committee_links = [(a.attrib['href']) for a in page.xpath('//table[@id="list"]//td[@class="db"]/a')]

            for link in committee_links:
                page = self.lxmlize(link)
                script_text = page.xpath('//head/script[not(@src)]/text()')[0]
                committee_name = re.search(r'var decisionBodyName = "(.*)";', script_text).group(1)
                committee_code = re.search(r'meetingRefs\.push\("[0-9]{4}\.([A-Z]{2})[0-9]+"\);', script_text).group(1)

                data = {'name': committee_name, 'code': committee_code, 'source_url': link}
                codes.update({committee_name: committee_code})

            # Manually add our renaming exception.
            codes.update({'Toronto City Council': 'CC'})

        return codes

    def full_identifiers(self, meeting_id, is_council=False, url=None):
        if not url:
            template = AGENDA_LIST_COUNCIL_TEMPLATE if is_council else AGENDA_LIST_STANDARD_TEMPLATE
            url = template.format(meeting_id)

        page = self.lxmlize(url)
        for a in page.xpath('//table[@class="itemTable"]//td[@class="itemNum"]//a'):
            link = a.attrib['href']
            full_identifier = parse_qs(urlparse(link).query)['item'][0]
            yield full_identifier
