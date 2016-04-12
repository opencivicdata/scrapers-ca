from __future__ import unicode_literals
from utils import CanadianScraper

from pupa.scrape import Bill, Event
from urllib.parse import parse_qs, urlparse
import lxml.html
import datetime as dt
import pytz
import re

from .helpers import (
    committees_from_sessions,
    build_lookup_dict,
)

from .constants import (
    CALENDAR_DAY_TEMPLATE,
    AGENDA_FULL_STANDARD_TEMPLATE,
    AGENDA_LIST_STANDARD_TEMPLATE,
    AGENDA_FULL_COUNCIL_TEMPLATE,
    AGENDA_LIST_COUNCIL_TEMPLATE,
    AGENDA_ITEM_TEMPLATE,
)


STATUS_DICT = {
    'Scheduled': 'confirmed',
    'Scheduled (Preview)': 'confirmed',
    'Complete': 'passed',
    'Cancelled': 'cancelled',
    'No Quorum': 'cancelled',
    'In Recess (will Resume)': 'confirmed',
    'In Progress (Public Session)': 'confirmed',
}

agenda_item_re = re.compile(r'reference = "(?P<identifier>.+?)";')
address_re = re.compile(r'codeAddress\("\d", ".+?". "(?P<address>.+?)"')


class TorontoIncrementalEventScraper(CanadianScraper):

    def __init__(self, jurisdiction, datadir, strict_validation=True, fastmode=False):
        super(TorontoIncrementalEventScraper, self).__init__(jurisdiction, datadir, strict_validation=True, fastmode=False)
        # Used to store mappings of committee names to two-letter codes
        self.committees_by_name = {}
        self.seen_agenda_items = []

    def scrape(self):
        today = dt.datetime.today()
        delta_days = 7
        start_date = today - dt.timedelta(days=delta_days)
        end_date = today + dt.timedelta(days=delta_days * 2)

        self.scrape_committee_data()
        yield from self.scrape_events_range(start_date, end_date)

    def scrape_committee_data(self):
        self.committees_by_name = self.committee_lookup_dict()

    def parse_table(self, table_node):
        items = []

        def sanitize_key(str):
            return str.lower().strip().replace(' ', '_').replace('.', '')

        def sanitize_org_name(org_name):
            # Some meetings preceded with legend, ie "S:" for special meetings.
            org_name = re.sub(r'^[A-Z]: +', '', org_name)
            # Strip suffix (ie. cancelled meetings)
            org_name = re.sub(r'\u2014.*$', '', org_name)
            org_name = org_name.strip()
            # Special case for city council name
            org_name = self.jurisdiction.name if org_name == 'City Council' else org_name
            return org_name

        rows = table_node.xpath('tr')
        headers = [sanitize_key(col.text) for col in rows.pop(0)]
        for row in rows:
            meeting_link = row.cssselect('a')[0].attrib['href']
            values = [col.text_content().strip() for col in row]
            item = dict(zip(headers, values))
            item.update({'meeting': sanitize_org_name(item['meeting'])})
            item.update({'meeting_link': meeting_link})
            items.append(item)

        return items

    def extract_events_by_url(self, calendar_day_url):
        page = self.lxmlize(calendar_day_url)

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
            calendar_day_url = CALENDAR_DAY_TEMPLATE.format(date.year, date.month - 1, date.day)
            events = self.extract_events_by_url(calendar_day_url)
            for event in events:
                tz = pytz.timezone("America/Toronto")
                time = dt.datetime.strptime(event['time'], '%I:%M %p')
                start = tz.localize(date.replace(hour=time.hour, minute=time.minute, second=0, microsecond=0))
                org_name = event['meeting']
                e = Event(
                    name=org_name,
                    start_time=start,
                    timezone=tz.zone,
                    location_name=event['location'],
                    status=STATUS_DICT.get(event['meeting_status'])
                )
                e.extras = {
                    'meeting_number': event['no'],
                    'tmmis_meeting_id': event['meeting_id'],
                }
                e.add_source(calendar_day_url)
                e.add_participant(
                    name=org_name,
                    type='organization',
                )

                def is_agenda_available(event):
                    return event['publishing_status'] in ['Agenda Published', 'Minutes Published']

                def is_council(event):
                    return True if event['meeting'] == self.jurisdiction.name else False

                if is_agenda_available(event):
                    agenda_url_template = AGENDA_FULL_COUNCIL_TEMPLATE if is_council(event) else AGENDA_FULL_STANDARD_TEMPLATE
                    agenda_url = agenda_url_template.format(event['meeting_id'])
                    full_identifiers = list(self.full_identifiers(event['meeting_id'], is_council(event)))

                    event_map_url_template = 'http://app.toronto.ca/tmmis/getAddressList.do?function=getMeetingAddressList&meetingId={}'
                    event_map_url = event_map_url_template.format(event['meeting_id'])
                    addresses_d = self.addressesByAgendaId(event_map_url)

                    e.add_source(agenda_url)
                    agenda_items = self.agenda_from_url(agenda_url)
                    for i, item in enumerate(agenda_items):

                        a = e.add_agenda_item(item['title'])
                        a.add_classification(item['type'].lower())
                        a['order'] = str(i)

                        def normalize_wards(raw):
                            if not raw:
                                raw = 'All'
                            if raw == 'All':
                                return raw.lower()
                            else:
                                return raw.split(', ')

                        wards = normalize_wards(item['wards'])
                        identifier_regex = re.compile(r'^[0-9]{4}\.([A-Z]{2}[0-9]+\.[0-9]+)$')
                        [full_identifier] = [id for id in full_identifiers if identifier_regex.match(id).group(1) == item['identifier']]
                        a.add_bill(full_identifier)
                        if full_identifier not in self.seen_agenda_items:
                            b = Bill(
                                # TODO: Fix this hardcode
                                legislative_session='2014-2018',
                                identifier=full_identifier,
                                title=item['title'],
                                from_organization={'name': self.jurisdiction.name},
                            )
                            b.add_source(agenda_url)
                            b.add_document_link(note='canonical', media_type='text/html', url=AGENDA_ITEM_TEMPLATE.format(full_identifier))
                            b.extras['wards'] = wards

                            addresses = addresses_d.get(full_identifier)
                            if addresses:
                                b.extras['locations'] = []
                                for address in addresses:
                                    location = {'address': {'full_address': address}}
                                    b.extras['locations'].append(location)

                            self.seen_agenda_items.append(full_identifier)

                            yield b

                yield e

    def agenda_from_url(self, url):
        page = self.lxmlize(url)
        main = page.xpath('//table[1]/..')[0]
        top_level_elems = main.getchildren()
        section_breaks = page.cssselect('table.border')

        section_break_indices = [i for i, elem in enumerate(top_level_elems) if elem in section_breaks]

        def partition(alist, indices):
            return [alist[i:j] for i, j in zip([0] + indices, indices + [None])]

        sections = partition(top_level_elems, section_break_indices)

        def treeify_section_list(section):
            tree = lxml.html.Element('section')
            for elem in section:
                tree.append(elem)

            return tree

        section_trees = [treeify_section_list(section) for section in sections]

        preamble = section_trees.pop(0)  # NOQA
        agenda_items = section_trees

        items = []
        newline_regex = re.compile(r' ?\r\n ?')
        for item in agenda_items:
            dict = {
                'identifier': item.xpath('//table[1]//td[1]')[0].text_content(),
                'type': item.xpath('//table[1]//td[2]')[0].text_content().strip(),
                'wards': item.xpath('//table[1]//td[5]')[0].text_content().strip().replace('Ward:', ''),
                'title': newline_regex.sub(' ', item.xpath('//table[2]//td[1]')[0].text_content().strip()),
            }

            items.append(dict)

        return items

    def committee_lookup_dict(self):
        # reversed so that most recent first
        sessions = reversed(self.jurisdiction.legislative_sessions)
        committee_term_instances = committees_from_sessions(self, sessions)
        committees_by_name = build_lookup_dict(self, data_list=committee_term_instances, index_key='name')
        # Manually add our City Council exception.
        committees_by_name.update({self.jurisdiction.name: [{'code': 'CC'}]})

        return committees_by_name

    def full_identifiers(self, meeting_id, is_council=False, url=None):
        if not url:
            template = AGENDA_LIST_COUNCIL_TEMPLATE if is_council else AGENDA_LIST_STANDARD_TEMPLATE
            url = template.format(meeting_id)

        page = self.lxmlize(url)
        for a in page.xpath('//table[@class="itemTable"]//td[@class="itemNum"]//a'):
            link = a.attrib['href']
            full_identifier = parse_qs(urlparse(link).query)['item'][0]
            yield full_identifier

    def addressesByAgendaId(self, meeting_map_url):
        addresses_d = {}

        page = self.lxmlize(meeting_map_url)
        script_text = page.xpath('//script[not(@src)]')[0].text_content()

        agenda_item_ids = re.findall(agenda_item_re, script_text)
        addresses = re.findall(address_re, script_text)

        for id, address in zip(agenda_item_ids, addresses):
            if not addresses_d.get(id):
                addresses_d[id] = [address]
            else:
                addresses_d[id].append(address)

        return addresses_d
