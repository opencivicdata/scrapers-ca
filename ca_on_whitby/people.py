from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.whitby.ca/en/townhall/meetyourcouncil.asp'


class WhitbyPersonScraper(CanadianScraper):

    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        person_elems = page.xpath('//tr')
        for person in person_elems:
            if len(person) > 1:
                info = person[1]
                try:  # Mayor and regional councillors
                    name, role = info[0].text_content().split(',')
                    role = role.strip()
                    if role == 'Deputy Mayor':
                        role = 'Regional Councillor'
                    if role == 'Regional Councillor':
                        district = 'Whitby (seat %d)' % regional_councillor_seat_number
                        regional_councillor_seat_number += 1
                    else:
                        district = 'Whitby'
                except ValueError:
                    district = ' '.join(info[0].text_content().split()[:2])
                    name, role = info[1].text_content().split(', ')
                email = self.get_email(info)
                image = person.xpath('.//img/@src')[0]
                p = Person(primary_org='legislature', name=name, district=district, role=role, image=image)
                p.add_source(COUNCIL_PAGE)
                p.add_contact('email', email)
                yield p
