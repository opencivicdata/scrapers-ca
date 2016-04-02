from __future__ import unicode_literals

from collections import defaultdict
from pupa.scrape import Bill
from utils import CanadianScraper
from lxml.etree import tostring

import datetime
import lxml.etree as etree
import pytz
import re

# TODO: Create ticket to move lxmlize into pupa.scrape.Base

ACTION_CLASSIFICATION = {
        'Adopted' : 'passage',
        'Adopted on Consent' : 'passage',
        'Amended' : 'amendment-amended',
        'Confirmed' : 'confirmed',
        'Deferred' : 'deferred',
        'Deferred Indefinitely': 'deferred',
        'Intro Failed' : None,
        'No Action' : None,
        'No Quorum' : 'failure',
        'Not Adopted' : None,
        'Noted/Filed' : 'filing',
        'Received' : None,
        'Referred' : 'committee-referral',
        'Recinded' : 'failure',
        'Withdrawn' : 'withdrawal',
        'Without Recs' : None,
        'Waive Referral' : None,
        }

class TorontoNewBillScraper(CanadianScraper):

    DEFAULT_START_DATE = datetime.datetime(2014, 1, 1)
    AGENDA_ITEM_SEARCH_URL = 'http://app.toronto.ca/tmmis/findAgendaItem.do?function=doSearch&fromDate=2016-02-22&toDate=2016-02-22&itemsPerPage=1000'
    AGENDA_ITEM_URL_TEMPLATE = 'http://app.toronto.ca/tmmis/viewAgendaItemHistory.do?item={}'

    TIMEZONE = 'America/Toronto'
    date_format='%B %d, %Y'

    def scrape(self):
        for agenda_item in self.agendaItems(updated_after=self.DEFAULT_START_DATE):
            # TODO: Add agenda_item type to OCD
            leg_type = 'bill'
            b = Bill(
                    identifier=agenda_item['Item No.'],
                    title=agenda_item['Title'],
                    legislative_session=None,
                    classification=leg_type,
                    from_organization={'name': self.jurisdiction.name},
                    )
            b.add_source(agenda_item['url'], note='web')

            # TODO: Fake session for now
            b.legislative_session = '2014-2018'

            agenda_item_versions = self.agendaItemVersions(agenda_item['url'])

            for version in agenda_item_versions:
                action_description = version['action']
                action_date = self.toDate(version['date'])
                responsible_org = version['responsible_org']
                action_class = ACTION_CLASSIFICATION[version['action']]

                if responsible_org == 'City Council':
                    responsible_org = self.jurisdiction.name

                act = b.add_action(action_description,
                                      action_date,
                                      organization={'name': responsible_org},
                                      classification=action_class)

            yield b
            #history = agenda_item_details['history']

    def agendaItems(self, updated_after=None, updated_before=None):
        for agenda_item_summary in self.searchAgendaItems(updated_after, updated_before) :
            yield agenda_item_summary

    def searchAgendaItems(self, date_from=None, date_to=None):
        """
        Submit a search query on the agenda item search page, and return a list
        of result pages.
        """
        page = self.lxmlize(self.AGENDA_ITEM_SEARCH_URL)
        for agenda_item_summary in self.parseSearchResults(page):
            yield agenda_item_summary

    def parseSearchResults(self, page) :
        """Take a page of search results and return a sequence of data
        of tuples about the agenda_item, of the form

        TODO: Fix column names
        ('Document ID', 'Document URL', 'Type', 'Status', 'Introduction Date'
        'Passed Date', 'Main Sponsor', 'Title')
        """
        table = page.xpath("//table[@id='searchResultsTable']")[0]
        for agenda_item, headers, _ in self.parseDataTable(page):
            id_key = headers[1]

            agenda_item_id = agenda_item[id_key]['label']
            agenda_item[id_key] = agenda_item_id

            agenda_item_url = self.AGENDA_ITEM_URL_TEMPLATE.format(agenda_item_id)
            agenda_item['url'] = agenda_item_url

            yield agenda_item

    def agendaItemVersions(self, agenda_item_url):
        page = self.lxmlize(agenda_item_url)
        versions = []
        for version in self.parseAgendaItemVersions(page):
            versions.append(version)

        return versions

    def parseAgendaItemVersions(self, page):
        script_text = page.xpath('//head/script[not(@src)]/text()')[0]
        index_qs = re.findall(r'if\(index == (\d)\){', script_text)
        function_qs = re.findall(r'var f = "(.*)";', script_text)
        agenda_item_id_qs = re.findall(r'agendaItemId:"(.*)"', script_text)
        url_template = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function={}&agendaItemId={}'
        for i, f, id in zip(index_qs, function_qs, agenda_item_id_qs):
            agenda_item_version_url = url_template.format(f, id)
            version = self.agendaItemVersion(agenda_item_version_url)

            xpr = '//div[@id="header{}"]'.format(i)
            header = page.xpath(xpr)[0].text_content()
            header_re = re.compile('^(.+) consideration on (.+)$')
            org, date = re.match(header_re, header).groups()
            version.update({
                'responsible_org': org,
                'date': date,
                })
            yield version

    def parseDataTable(self, table):
        """
        Legistar uses the same kind of data table in a number of
        places. This will return a list of dictionaries using the
        table headers as keys.
        """
        headers = table.xpath(".//th")
        rows = table.xpath(".//tr[@class='hoverOver']")

        keys = []
        for header in headers :
            text_content = header.text_content().replace('&nbsp;', ' ').strip()
            if text_content :
                keys.append(text_content)
            else :
                keys.append(header.xpath('.//input')[0].value)

        for row in rows:
            try:
                data = defaultdict(lambda : None)

                for key, field in zip(keys, row.xpath("./td")):
                    text_content = self._stringify(field)

                    if field.find('.//a') is not None :
                        address = self._get_link_address(field.find('.//a'))
                        if address :
                            if key == '' and 'View.ashx?M=IC' in address :
                                req = self.get(address, verify=False)
                                value = icalendar.Calendar.from_ical(req.text)
                                key = 'iCalendar'
                            else :
                                value = {'label': text_content, 
                                         'url': address}
                        else :
                            value = text_content
                    else :
                        value = text_content

                    data[key] = value

                yield data, keys, row

            except Exception as e:
                print('Problem parsing row:')
                print(etree.tostring(row))
                print(traceback.format_exc())
                raise e

    def _get_link_address(self, link):
        url = None
        if 'onclick' in link.attrib:
            onclick = link.attrib['onclick']
            if (onclick is not None 
                and onclick.startswith(("radopen('",
                                        "window.open",
                                        "OpenTelerikWindow"))):
                url = self.BASE_URL + onclick.split("'")[1]
        elif 'href' in link.attrib : 
            url = link.attrib['href']

        return url

    def _stringify(self, field) :
        for br in field.xpath("*//br"):
            br.tail = "\n" + br.tail if br.tail else "\n"
        for em in field.xpath("*//em"):
            if em.text :
                em.text = "--em--" + em.text + "--em--"
        return field.text_content().replace('&nbsp;', ' ').strip()

    def agendaItemVersion(self, agenda_item_version_url):
        """
        Details:
            * title
            * sponsors (when Member Motions [MM], primary & secondary from title)
            * type
            * ward(s)

        Possible sections: 
            * [ Board | Community Council | Committee ] Decision Advice and Other Information
            * Origin
            * [ Board | Community Council | Committee ] Recommendations
            * Summary
            * Financial Impact
            * Background Information [ (Board | Community Council | Committee | City Council) ] (parsed)
            * Speakers
            * Communications [ (Board | Community Council | Committee | City Council) ] (parsed)
            * Declared Interests [ (Board | Community Council | Committee | City Council) ]
            * Subsections? (recursive)
            * Motions (parsed)
                * Votes (optional)
            * Rulings (parsed) Ex: http://app.toronto.ca/tmmis/viewAgendaItemHistory.do?item=2016.EY12.29
                * Votes (optional on challenge)

        TODO: Investigate "Bills and By-law" [BL] code for bill context
        """
        page = self.lxmlize(agenda_item_version_url)
        version = {}
        version.update({
            'type': page.xpath("//table[@class='border'][1]//td[2]")[0].text_content().strip().lower(),
            'action': page.xpath("//table[@class='border'][1]//td[3]")[0].text_content().strip(),
            })

        wards = page.xpath("//table[@class='border'][1]//td[5]")[0].text_content().strip().lower()
        wards_re = re.compile('ward:(.*)')
        matches = re.match(wards_re, wards)
        if matches:
            wards = matches.group(1)
            if wards != 'all':
                wards = wards.split(', ')
        else:
            wards = 'all'

        version.update({'wards': wards})

        title = page.xpath("//table[.//font[@face='Arial' and @size=4]][1]")[0].text_content().strip()
        title_re = re.compile('^(.+?)(?: - (?:by )?((?:Deputy )?Mayor|Councillor) (.+), seconded by ((?:Deputy )?Mayor|Councillor) (.+))?$')
        title, primary_role, primary_sponsor, secondary_role, secondary_sponsor = re.match(title_re, title).groups()
        version.update({'title': title})
        version.update({'sponsors': {'primary': primary_sponsor, 'secondary': secondary_sponsor}})

        section_nodes = page.xpath("//table[@width=620 and .//font[@face='Arial' and @size=3] and .//tr[3]]")
        sections = {}
        for node in section_nodes:
            section_title = node.find('.//tr[1]/td//font/b').text_content().strip()
            section_content = node.find('.//tr[2]/td')
            sections[section_title] = section_content.text_content()

        if 'Motions' in sections:
            sections['Motions'] = self.parseAgendaItemVersionMotions(sections['Motions'])

        version.update({'sections': sections})

        return version

    def parseAgendaItemVersionMotions(self, motions_section):
        return motions_section

    def toTime(self, text) :
        time = datetime.datetime.strptime(text, self.date_format)
        time = pytz.timezone(self.TIMEZONE).localize(time)
        return time

    def toDate(self, text) :
        return self.toTime(text).date().isoformat()
