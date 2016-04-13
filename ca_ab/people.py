from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import csv

import lxml.html

COUNCIL_PAGE = 'http://www.assembly.ab.ca/net/index.aspx?p=mla_csv'

PARTIES = {
    'AP': 'Alberta Party',
    'AL': 'Alberta Liberal Party',
    'ND': 'Alberta New Democratic Party',
    'PC': 'Progressive Conservative Association of Alberta',
    'W': 'Wildrose Alliance Party',
    'IND': 'Independent',
}


def get_party(abbr):
    """Return full party name from abbreviation"""
    return PARTIES[abbr]


class AlbertaPersonScraper(CanadianScraper):

    def scrape(self):
        csv_text = self.get(self.get_csv_url()).text
        cr = csv.DictReader(csv_text.split('\n'))
        for mla in cr:
            name = '{} {} {}'.format(mla['MLA First Name'], mla['MLA Middle Names'], mla['MLA Last Name'])
            if name.strip() == '':
                continue
            party = get_party(mla['Caucus'])
            name_without_status = name.split(',')[0]
            detail_url = (
                'http://www.assembly.ab.ca/net/index.aspx?'
                'p=mla_contact&rnumber={0}&leg=29'.format(
                    mla['Riding Number']
                )
            )
            detail_page = self.lxmlize(detail_url)
            photo_url = detail_page.xpath('//img[@class="MemPhoto"]/@src')[0]
            p = Person(
                primary_org='legislature',
                name=name_without_status,
                district=mla['Riding Name'],
                role='MLA',
                party=party,
                image=photo_url,
            )
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            if mla['Email']:
                p.add_contact('email', mla['Email'])
            elif mla['MLA Email']:
                p.add_contact('email', mla['MLA Email'])
            if mla['Phone Number']:
                p.add_contact('voice', mla['Phone Number'], 'legislature')
            yield p

    def get_csv_url(self):
        csv_gen_page = self.lxmlize(COUNCIL_PAGE)

        # ASP forms store session state. Looks like we can't just play back a POST.
        get_hidden_val = lambda v: csv_gen_page.xpath('//input[@id="{}"]/@value'.format(v))[0]
        post_data = {
            '__VIEWSTATE': get_hidden_val('__VIEWSTATE'),
            '__VIEWSTATEGENERATOR': get_hidden_val('__VIEWSTATEGENERATOR'),
            '__EVENTVALIDATION': get_hidden_val('__EVENTVALIDATION'),
            '_ctl0:radlstGroup': 'Information for All MLAs',
            '_ctl0:chklstFields:0': 'on',
            '_ctl0:chklstFields:1': 'on',
            '_ctl0:chklstFields:2': 'on',
            '_ctl0:btnCreateCSV': "Create '.csv' file",
        }

        resp = self.post(COUNCIL_PAGE, data=post_data)
        result_page = lxml.html.fromstring(resp.text)
        return result_page.xpath('//a[@id="_ctl0_HL_file"]/@href')[0]
