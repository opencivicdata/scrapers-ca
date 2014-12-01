from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.coquitlam.ca/city-hall/mayor-and-council/mayor-and-council.aspx'


class CoquitlamPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        for person_link in page.xpath('//a[@class="L4"]'):
            role, name = person_link.text_content().split(' ', 1)
            url = person_link.attrib['href']
            page = self.lxmlize(url)
            photo_url = page.xpath('//img[@class="img-right"]/@src')[0]
            email = page.xpath('//a[starts-with(@href, "mailto:")]//text()')[0]

            if role == 'Mayor':
                district = 'Coquitlam'
            else:
                district = 'Coquitlam (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p
