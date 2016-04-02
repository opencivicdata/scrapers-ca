from __future__ import unicode_literals

from collections import defaultdict
from pupa.scrape import Bill
from utils import CanadianScraper
from lxml.etree import tostring

import lxml.etree as etree
import datetime
import re

# TODO: Create ticket to move lxmlize into pupa.scrape.Base

ACTION_CLASSIFICATION = {
        'Adopted' : None,
        'Adopted on Consent' : None,
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
    AGENDA_ITEM_SEARCH_URL = 'http://app.toronto.ca/tmmis/findAgendaItem.do?function=doSearch&fromDate=2016-03-31&toDate=2016-03-31&itemsPerPage=1000'
    AGENDA_ITEM_URL_TEMPLATE = 'http://app.toronto.ca/tmmis/viewAgendaItemHistory.do?item={}'

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

            agenda_item_details = self.agendaItemDetails(agenda_item['url'])

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

    def agendaItemDetails(self, agenda_item_url):
        page = self.lxmlize(agenda_item_url)
        versions = []
        for agenda_item_version_url in self.parseAgendaItemIds(page):
            version = self.agendaItemVersion(agenda_item_version_url)
            versions.append(version)

    def parseAgendaItemIds(self, page):
        script_text = page.xpath('//head/script[not(@src)]/text()')[0]
        function_qs = re.findall(r'var f = "(.*)";', script_text)
        agenda_item_id_qs = re.findall(r'agendaItemId:"(.*)"', script_text)
        url_template = 'http://app.toronto.ca/tmmis/viewAgendaItemDetails.do?function={}&agendaItemId={}'
        for f, id in zip(function_qs, agenda_item_id_qs):
            agenda_item_version_url = url_template.format(f, id)
            yield agenda_item_version_url

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
            * identifier
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
        identifier = page.xpath("//table[@class='border'][1]//td[1]")[0].text_content().strip()
        item_type = page.xpath("//table[@class='border'][1]//td[2]")[0].text_content().strip().lower()
        action = page.xpath("//table[@class='border'][1]//td[3]")[0].text_content().strip()

        wards = page.xpath("//table[@class='border'][1]//td[5]")[0].text_content().strip().lower()
        wards_re = re.compile('ward:(.*)')
        #wards = re.match(wards_re, wards).group(0)
        wards = re.match(wards_re, wards).group(1)
        if wards != 'all':
            wards = wards.split(', ')

        title = page.xpath("//table[.//font[@face='Arial' and @size=4]][1]")[0].text_content().strip()
        title_re = re.compile('^(.*)(?: - by ((?:Deputy )?Mayor|Councillor) (.*), seconded by ((?:Deputy )?Mayor|Councillor) (.*))?$')
        matches = re.match(title_re, title)
        title, primary_role, primary_sponsor, secondary_role, secondary_sponsor = re.match(title_re, title).groups()

        sections = page.xpath("//table[@width=620 and .//font[@face='Arial' and @size=3] and .//tr[3]]")
        version = {}
        for section in sections:
            section_title = section.find('.//tr[1]/td//font/b').text_content().strip()
            section_content = section.find('.//tr[2]/td')
            version[section_title] = section_content

        if 'Motions' in sections:
            version['Motions'] = self.parseAgendaItemVersionMotions(version['Motions'])

        return version

    def _parseVersionNumbers(self, inline_script_tag):
        # TODO: return list of 
        return []
