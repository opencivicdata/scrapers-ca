from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person
from pupa.scrape import Organization
from lxml.etree import ParserError

from people_helpers import normalize_org_name, get_parent_committee, format_date, normalize_person_name

import re
import json

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'
AGENDA_SEARCH_PAGE = 'http://app.toronto.ca/tmmis/findAgendaItem.do?function=doPrepare'
COMMITTEE_PAGE_TEMPLATE = 'http://app.toronto.ca/tmmis/decisionBodyProfile.do?function=doPrepare&decisionBodyId={}'

APPOINTMENTS_ENDPOINT = 'https://secure.toronto.ca/pa/appointment/listJtable.json?jtPageSize=2000'

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

        def to_dict(opt):
            name, term = re.search('^(.+) \((\d{4}-\d{4})\)$', opt.text).groups()
            decision_body_id = opt.attrib['value']
            return {
                'name': normalize_org_name(name),
                'term': term,
                'id': decision_body_id,
            }

        committee_sessions = [to_dict(opt) for opt in committee_options if has_value(opt)]
        for session in committee_sessions:
            parent_name = get_parent_committee(session['name'])
            if parent_name:
                o = Organization(name=session['name'], classification='committee', parent_id={'name': parent_name})
                o.add_source(COMMITTEE_PAGE_TEMPLATE.format(session['id']))
            else:
                o = Organization(name=session['name'], classification='committee', parent_id={'classification': 'legislature'})

            o.add_source(AGENDA_SEARCH_PAGE)
            o.add_source(APPOINTMENTS_ENDPOINT)

            try:
                members = self.fetch_members_from_id(session['id'])
            except ParserError:
                members = []

            member_names = [m['name'] for m in members]
            for name in member_names:
                o.add_member(name)
            yield o

    def scrape_people(self):
        yield from self.scrape_appointees()
        yield from self.scrape_council()

    def scrape_appointees(self):
        response = self.post(APPOINTMENTS_ENDPOINT)
        json_data = json.loads(response.text)

        for record in json_data['Records']:
            if record['role'] in ["Member"]:
                person_name = normalize_person_name(record['memberName'])
                p = Person(name=person_name, role=record['role'], district=self.jurisdiction.division_name)
                p.add_source(APPOINTMENTS_ENDPOINT)

                org_name = normalize_org_name(record['decisionBodyName'])
                parent_name = get_parent_committee(org_name)
                if parent_name:
                    o = Organization(name=org_name, classification='committee', parent_id={'name': parent_name})
                else:
                    o = Organization(name=org_name, classification='committee', parent_id={'classification': 'legislature'})

                o.add_source(AGENDA_SEARCH_PAGE)
                o.add_source(APPOINTMENTS_ENDPOINT)

                start_date = format_date(record['appointmentStartDate'])
                end_date = format_date(record['appointmentEndDate'])
                o.add_member(p, role=record['role'], start_date=start_date, end_date=end_date)

                yield p
                yield o

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
        if scraper_broken:
            name = 'John Tory'
            p = Person(primary_org='legislature', name=name, district="Toronto", role='Mayor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            yield p
            return

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

    def build_url_from_id(self, url_template, decision_body_id=None, meeting_id=None):
        if decision_body_id is not None:
            url = url_template.format('decisionBodyId', decision_body_id)
        elif meeting_id is not None:
            url = url_template.format('meetingId', meeting_id)
        else: raise

        return url

    def fetch_members_from_id(self, decision_body_id=None, meeting_id=None):
        url_template = 'http://app.toronto.ca/tmmis/decisionBodyProfile.do?function=doGetMembers&{}={}'
        url = self.build_url_from_id(url_template, decision_body_id, meeting_id)

        return self.fetch_members_from_url(url)

    def fetch_members_from_url(self, url):
        tree = self.lxmlize(url)

        fields = {
                'name': {
                    'pattern': 'li',
                    'type': 'string',
                    },
                'is_chair': {
                    'pattern': 'li strong:nth-of-type(1)',
                    'type': 'bool',
                    },
                'is_vice': {
                    'pattern': 'li strong:nth-of-type(2)',
                    'type': 'bool',
                    },
                }

        def has_position(x): return False if x == None else True

        data = {}
        for name, conf in fields.items():
            type_ = conf['type']
            pattern = conf['pattern']
            if type_ == 'string':
                data[name] = [result.text.strip() for result in tree.cssselect(pattern)]
            if type_ == 'bool':
                data[name] = [has_position(result.text) for result in tree.cssselect(pattern)]

        items = []
        number_of_results = min([len(n) for n in data.values()])
        for i in range(number_of_results):
            item = {}
            for key in data.keys():
                item.update({ key : data[key][i] })
            items.append(item)

        return items
