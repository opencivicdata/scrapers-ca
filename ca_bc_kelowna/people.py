from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.kelowna.ca/CM/Page159.aspx'


class KelownaPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        links = page.xpath('//td[@width=720]//a[contains(text(), "Councillor") or contains(text(), "Mayor")]')
        for link in links:
            role, name = link.text_content().replace('\xa0', ' ').split(' ', 1)
            url = link.attrib['href']
            page = self.lxmlize(url)
            photo_url = page.xpath('//li/img/@src')[0]
            phone = page.xpath('//strong')[-1].text_content()
            email = self.get_email(page)

            if role == 'Mayor':
                district = 'Kelowna'
            else:
                district = 'Kelowna (seat %d)' % councillor_seat_number
                councillor_seat_number += 1

            p = Person(primary_org='legislature', name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)
            yield p
