from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.saanich.ca/living/mayor/council/index.html'


class SaanichPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        for link in page.xpath('//div[@class="section"]//a'):
            url = link.attrib['href']
            if url.endswith('address.pdf'):
                continue
            page = self.lxmlize(url)
            role, name = page.xpath('//div[@id="content"]/h1//text()')[0].split(' ', 1)
            photo_url = page.xpath('//div[@id="content"]//@src')[0]
            email = self.get_email(page)

            if role == 'Mayor':
                district = 'Saanich'
            else:
                district = 'Saanich (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('email', email)
            yield p
