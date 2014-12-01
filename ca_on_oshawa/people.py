from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.oshawa.ca/cit_hall/council4.asp'


class OshawaPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        mayor_table, council_table = page.xpath('//table')[:2]
        rep_cells = mayor_table.xpath('.//td[1]') + council_table.xpath('.//td[h4]')
        for rep_cell in rep_cells:
            name, role, phone = [elem.text for elem in rep_cell]
            if name.startswith('Mayor '):
                name = name[len('Mayor '):]
            email = rep_cell.xpath('string(.//a)')
            photo_url = rep_cell.xpath('./following-sibling::td[1]/img/@src')[0]

            if role == 'City Councillor':
                role = 'Councillor'
                district = 'Oshawa (seat %d)' % councillor_seat_number
                councillor_seat_number += 1
            elif role == 'Regional and City Councillor':
                role = 'Regional Councillor'
                district = 'Oshawa (seat %d)' % regional_councillor_seat_number
                regional_councillor_seat_number += 1
            else:
                district = 'Oshawa'

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
