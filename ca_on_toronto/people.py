from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person
from .helpers import (
    committees_from_sessions,
    build_lookup_dict,
    )

from pupa.scrape import Organization

import re
from .constants import (
    COMMITTEE_LIST_TEMPLATE,
    TWO_LETTER_ORG_CODE_SCHEME,
    )

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'


OTHER_NAMES = {
    'Norm Kelly': ['Norman Kelly'],
    'Justin Di Ciano': ['Justin J. Di Ciano'],
}


class TorontoPersonScraper(CanadianScraper):

    def scrape(self):
        yield from self.scrape_committees()
        yield from self.scrape_people()

    def scrape_committees(self):
        sessions = reversed(self.jurisdiction.legislative_sessions)
        committee_term_instances = committees_from_sessions(self, sessions)
        committees_by_code = build_lookup_dict(self, data_list=committee_term_instances, index_key='code')

        for code, instances in committees_by_code.items():
            # TODO: Figure out how to edit city council org.
            if code == 'CC': continue


            extras = { 'tmmis_decision_body_ids': [] }
            for i, inst in enumerate(instances):
                # TODO: Ensure this survives addition of new term (2017)
                #       so specific year always creates
                canonical_i = 0
                if i == canonical_i:
                    o = Organization(
                        name=inst['name'],
                        classification='committee',
                        )
                    extras.update({ 'description': inst['info'] })
                    o.add_identifier(inst['code'], scheme=TWO_LETTER_ORG_CODE_SCHEME)
                extras['tmmis_decision_body_ids'].append({ inst['term']: inst['decision_body_id'] })
                o.extras = extras
                o.add_source(inst['source_url'])
                if instances[canonical_i]['name'] != inst['name']:
                    # TODO: Add start_date and end_date
                    o.add_name(inst['name'])

            yield o

    def scrape_people(self):
        page = self.lxmlize(COUNCIL_PAGE)

        a = page.xpath('//a[contains(text(),"Mayor")]')[0]
        yield self.scrape_mayor(a.attrib['href'])

        for a in page.xpath('//table')[0].xpath('.//a[contains(text(),"Councillor")]'):
            page = self.lxmlize(a.attrib['href'])
            h1 = page.xpath('//h1//text()')[0]
            if 'Council seat is vacant' not in h1:
                yield self.scrape_councilor(page, h1, a.attrib['href'])

    def scrape_councilor(self, page, h1, url):
        name = h1.split('Councillor')[1].strip()
        ward_full = page.xpath('//p/descendant-or-self::*[contains(text(), "Profile:")]/text()')[0].replace('\xa0', ' ')
        ward_num, ward_name = re.search(r'(Ward \d+) (.+)', ward_full).groups()
        if ward_name == 'Etobicoke Lakeshore':
            ward_name = 'Etobicoke\u2014Lakeshore'

        district = '{0} ({1})'.format(ward_name.replace('-', '\u2014'), ward_num.split()[1])

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        for name in OTHER_NAMES.get(name, []):
            p.add_name(name)

        p.image = page.xpath('//main//img/@src')[0].replace('www.', 'www1.')  # @todo fix lxmlize to use the redirected URL to make links absolute
        email = self.get_email(page)
        p.add_contact('email', email)

        addr_cell = page.xpath('//*[contains(text(), "Toronto City Hall")]/ancestor::td')[0]
        phone = (addr_cell.xpath('(.//text()[contains(., "Phone:")])[1]')[0]
                          .split(':')[1])
        p.add_contact('voice', phone, 'legislature')

        address = '\n'.join(addr_cell.xpath('./p[2]/text()')[:2])
        if address:
            p.add_contact('address', address, 'legislature')

        return p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//meta[@property="og:description"]/@content')[0].replace('Office of the Mayor of Toronto, ', '').strip()

        p = Person(primary_org='legislature', name=name, district="Toronto", role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        p.image = page.xpath('//article/img/@src')[0].replace('www.', 'www1.')

        url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href'].replace('www.', 'www1.')
        p.add_source(url)
        page = self.lxmlize(url)

        mail_elem, email_elem, phone_elem = page.xpath('//article[contains(@class,"col-sm-6")]//header')[:3]
        address = ''.join(mail_elem.xpath('./following-sibling::p//text()'))
        phone = phone_elem.xpath('./following-sibling::p[1]//text()')[0]
        email = email_elem.xpath('./following-sibling::p[1]//text()')[0]

        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        return p
