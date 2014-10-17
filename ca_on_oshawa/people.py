# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.oshawa.ca/cit_hall/council4.asp'


class OshawaPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        mayor_table, council_table = page.xpath('//table')[:2]
        rep_cells = mayor_table.xpath('.//td[1]') + council_table.xpath('.//td[h4]')
        for rep_cell in rep_cells:
            name, role, phone = [elem.text for elem in rep_cell]
            if name.startswith('Mayor '):
                name = name[len('Mayor '):]
            email = rep_cell.xpath('string(.//a)')
            photo_url = rep_cell.xpath('string(./following-sibling::td[1]/img/@src)')

            if role == 'City Councillor':
                role = 'Councillor'
            elif role == 'Regional and City Councillor':
                role = 'Regional Councillor'

            p = Person(primary_org='legislature', name=name, district='Oshawa', role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
