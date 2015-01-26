from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.markham.ca/wps/portal/Markham/MunicipalGovernment/MayorAndCouncil/RegionalAndWardCouncillors/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOJN_N2dnX3CLAKNgkwMDDw9XcJM_VwCDUMDDfULsh0VAfz7Fis!/'


class MarkhamPersonScraper(CanadianScraper):

    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//a[contains(text(), "Office of the Mayor")]/@href')[0]
        yield self.scrape_mayor(mayor_url)

        councillors = page.xpath('//div[@class="interiorContentWrapper"]//td[./a]')
        for councillor in councillors:
            name_elem = ' '.join(councillor.xpath('.//strong/text()'))
            if 'Mayor' in name_elem:
                name = name_elem.split('Mayor')[1]
            elif 'Councillor' in name_elem:
                name = name_elem.split('Councillor')[1]
            else:
                name = name_elem

            district = councillor.xpath('.//a//text()[normalize-space()]')[0]
            if 'Ward' in district:
                district = district.replace('Councillor', '')
                role = 'Councillor'
            elif 'Regional' in district:
                role = 'Regional Councillor'
                district = 'Markham (seat %d)' % regional_councillor_seat_number
                regional_councillor_seat_number += 1
            else:
                role = district
                district = 'Markham'

            image = councillor.xpath('.//img/@src')[0]
            url = councillor.xpath('.//a/@href')[0]

            if 'Ward 4' in district or 'seat 3' in district or 'Ward 6' in district:
                yield self.scrape_4(name, url, image)
                continue

            page = self.lxmlize(url)

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = image
            contact = page.xpath('//div[@class="microSiteLinksWrapper"]')[1]

            if contact.xpath('.//p/text()'):
                infos = contact.xpath('.//p/text()')
            else:
                infos = contact.xpath('.//div/text()')

            address = re.sub(r'\s{2,}', ' ', ' '.join(infos[:2])).strip()
            phone = infos[2].split(':')[1].strip()
            email = self.get_email(contact)
            p.add_contact('address', address, 'legislature')
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('email', email)

            get_links(p, contact)
            yield p

    def scrape_4(self, name, url, image):
        page = self.lxmlize(url)

        p = Person(primary_org='legislature', name=name, district='Ward 4', role='Councillor')
        p.add_source(url)
        p.add_source(COUNCIL_PAGE)

        address = re.sub(r'\s{2,}', ' ', ' '.join(page.xpath('//div[@class="interiorContentWrapper"]/p[1]/text()')))
        phone = page.xpath('//div[@class="interiorContentWrapper"]/p[2]/text()')[0].split(':')[1].strip()
        email = self.get_email(page)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = image
        return p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//div[@class="interiorContentWrapper"]/p/strong/text()')[0]
        address = ' '.join(page.xpath('//div[@class="interiorContentWrapper"]/p/text()')[1:3])
        address = re.sub(r'\s{2,}', ' ', address)
        contact_elem = page.xpath('//div[@class="interiorContentWrapper"]/p[3]')[0]
        phone = contact_elem.text.split(':')[1].strip()
        email = self.get_email(contact_elem)

        p = Person(primary_org='legislature', name=name, district='Markham', role='Mayor')
        p.add_source(url)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        yield p


def get_links(councillor, div):
    links = div.xpath('.//a')
    for link in links:
        link = link.attrib['href']
        if 'mailto:' not in link and 'http://www.markham.ca' not in link:
            councillor.add_link(link)
