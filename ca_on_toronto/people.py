from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person
from pupa.scrape import Organization

import re

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'
AGENDA_SEARCH_PAGE = 'http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare'

SUBCOMMITTEES = {
    '^Budget Subcommittee ': 'Budget Committee',
    '^Interview Subcommittee for ': 'Civic Appointments Committee',
    '^Parks and Environment Subcommittee': 'Parks and Environment Committee',
    '^Toronto and East York Community Council ': 'Toronto and East York Community Council',
    'CDR Core Service Review Subcommittee': 'Community Development and Recreation Committee',
    'Holiday Shopping Subcommittee': 'Economic Development Committee',
    'SSO and Recycling Infrastructure Subcommittee': 'Public Works and Infrastructure Committee',
    'Seniors Strategy Subcommittee': 'Planning and Growth Management Committee',
    'Subcommittee on Establishment of Local Appeal Body': 'Planning and Growth Management Committee',
    'Subcommittee to Review Billy Bishop Airport Consultant Reports': 'Toronto and East York Community Council',
    'Tenant Issues Committee': 'Executive Committee',
    'Tenant Issues Subcommittee': 'Community Development and Recreation Committee',
}


class TorontoPersonScraper(CanadianScraper):

    def scrape(self):
        yield from self.scrape_organizations()
        yield from self.scrape_people()

    def scrape_organizations(self):
        yield from self.scrape_committees()

    def scrape_committees(self):
        page = self.lxmlize(AGENDA_SEARCH_PAGE)
        committee_options = page.xpath('//select[@id="decision_body"]/option')

        def has_value(opt): return bool(opt.text.strip())

        def normalize_name(name):
            name = re.sub(r'sub-?committee', 'Subcommittee', name,  flags=re.IGNORECASE)
            return name

        def to_dict(opt):
            name, term = re.search('^(.+) \((\d{4}-\d{4})\)$', opt.text).groups()
            external_id = opt.attrib['value']
            return {
                'name': normalize_name(name),
                'term': term,
                'id': external_id,
            }

        def get_parent_committee(child_name):
            for pattern, parent_name in SUBCOMMITTEES.items():
                if re.search(pattern, child_name): return parent_name

        committee_sessions = [to_dict(opt) for opt in committee_options if has_value(opt)]
        for session in committee_sessions:
            parent_name = get_parent_committee(session['name'])
            if parent_name:
                o = Organization(name=session['name'], classification='committee', parent_id={'name': parent_name})
                o.add_source('http://app.toronto.ca/tmmis/decisionBodyProfile.do?function=doPrepare&decisionBodyId={}'.format(session['id']))
            else:
                o = Organization(name=session['name'], classification='committee', parent_id={'classification': 'legislature'})
            o.add_source(AGENDA_SEARCH_PAGE)
            yield o

    def scrape_people(self):
        # yield from self.scrape_appointees()
        yield from self.scrape_council()

    def scrape_appointees(self):
        return

    def scrape_council(self):
        page = self.lxmlize(COUNCIL_PAGE)

        a = page.xpath('//a[contains(text(),"Mayor")]')[0]
        yield from self.scrape_mayor(a.attrib['href'])

        for a in page.xpath('//table')[0].xpath('.//a[contains(text(),"Councillor")]'):
            yield from self.scrape_councilor(a.attrib['href'])

    def scrape_councilor(self, url):
        page = self.lxmlize(url)
        h1 = page.xpath('//h1//text()')[0]
        if 'Council seat is vacant' in h1: return

        name = h1.split('Councillor')[1]
        ward_full = page.xpath('//p/descendant-or-self::*[contains(text(), "Profile:")]/text()')[0].replace('\xa0', ' ')
        ward_num, ward_name = re.search(r'(Ward \d+) (.+)', ward_full).groups()
        if ward_name == 'Etobicoke Lakeshore':
            ward_name = 'Etobicoke\u2014Lakeshore'

        district = '{0} ({1})'.format(ward_name.replace('-', '\u2014'), ward_num.split()[1])

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

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

        yield p

    def scrape_mayor(self, url):
        # TODO: Fix mayor scraper
        scraper_broken = True
        if scraper_broken: return

        page = self.lxmlize(url)
        name = page.xpath("//h1/text()")[0].replace("Toronto Mayor", "").strip()

        p = Person(primary_org='legislature', name=name, district="Toronto", role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        p.image = page.xpath('//article/img/@src')[0].replace('www.', 'www1.')

        url = page.xpath('//a[contains(text(), "Contact the Mayor")]')[0].attrib['href'].replace('www.', 'www1.')
        p.add_source(url)
        page = self.lxmlize(url)

        mail_elem, email_elem, phone_elem = page.xpath('//header')[:3]
        address = ''.join(mail_elem.xpath('./following-sibling::p//text()'))
        phone = phone_elem.xpath('./following-sibling::p[1]//text()')[0]
        email = email_elem.xpath('./following-sibling::p[1]//text()')[0]

        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        yield p
