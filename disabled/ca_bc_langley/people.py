from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.city.langley.bc.ca/index.php/city-hall/city-council'


class LangleyPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="menuitems"]/ul//li/a[contains(text(), "Councillor")]/@href')
        mayor = page.xpath('//div[@class="menuitems"]/ul//li/a[contains(text(), "Mayor")]/@href')[0]

        for url in councillors:
            district = 'Langley (seat %d)' % councillor_seat_number
            councillor_seat_number += 1
            yield self.scrape_councillor(url, district)

        yield self.scrape_mayor(mayor)

    def scrape_councillor(self, url, district):
        infos_page = self.lxmlize(url)
        infos = infos_page.xpath('//div[@class="item-page"]')[0]

        name = ' '.join(infos.xpath('p[2]/text()')[0].split(' ')[1:3])
        lname = name.lower()
        email = lname.split(' ')[0][0] + lname.split(' ')[1] + '@langleycity.ca'
        photo_url = infos.xpath('p[1]/img/@src')[0]

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)

        personal_infos = infos.xpath('p[last()]/text()')

        if 'Residence' in personal_infos[0]:
            phone = re.findall(r'(Phone|Res)(:?) (.*)', '\n'.join(personal_infos))[0][2]
            address = re.findall(r'Address: (.*) (Phone|Res)', ' '.join(personal_infos))[0][0]
            p.add_contact('address', address, 'residence')
            p.add_contact('voice', phone, 'residence')

        return p

    def scrape_mayor(self, url):
        infos_page = self.lxmlize(url)
        infos = infos_page.xpath('//div[@class="item-page"]')[0]

        name = ' '.join(infos.xpath('p[2]/text()')[0].split(' ')[2:4])
        lname = name.lower()
        email = lname.split(' ')[0][0] + lname.split(' ')[1] + '@langleycity.ca'
        photo_url = infos.xpath('p[1]/img/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Langley', role='Mayor', image=photo_url)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)

        personal_infos = infos.xpath('p[last()]/text()')

        phone = re.findall(r'Phone(:?) (.*)', '\n'.join(personal_infos))[0][1]
        address = re.findall(r'Address: (.*) Phone', ' '.join(personal_infos))[0]
        p.add_contact('address', address, 'office')
        p.add_contact('voice', phone, 'office')

        return p
