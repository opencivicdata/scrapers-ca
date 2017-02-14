from utils import CanadianScraper, CanadianPerson as Person

import re

COUNCIL_PAGE = 'http://www.town.caledon.on.ca/en/townhall/council.asp'


class CaledonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//div[@id="printAreaContent"]/ul/li/strong/a/@href')[0]
        yield self.scrape_mayor(mayor_url)

        councillors = page.xpath('//div[@id="printAreaContent"]//table//td')[2:]
        for councillor in councillors:
            district, name = councillor.text_content().split('-')
            url = councillor.xpath('.//a')[0].attrib['href']

            page = self.lxmlize(url)
            if 'Regional' in page.xpath('//h1')[0]:
                role = 'Regional Councillor'
            else:
                role = 'Area Councillor'

            p = Person(primary_org='legislature', name=name, district=district.strip(), role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            info = page.xpath('//table[@summary="Councillor"]/tbody/tr/td[2]')[0]
            info = info.text_content().strip().splitlines(True)
            info = [x for x in info if not x == '\xa0\n']
            address = info[1]
            email = re.findall(r'[a-z]+.[a-z]+@caledon.ca', info[2])[0]
            numbers = re.findall(r'[0-9]{3}.[0-9]{3}. ?[0-9]{4}', info[2])
            phone = numbers[0]
            fax = numbers[1]

            p.image = page.xpath('//table[@summary="Councillor"]//img/@src')[0]

            p.add_contact('address', address, 'legislature')
            p.add_contact('email', email)
            p.add_contact('voice', phone, 'legislature')
            p.add_contact('fax', fax, 'legislature')

            yield p

    def scrape_mayor(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//div[@id="printAreaContent"]/h1/strong/text()')[0].replace('Mayor', '').strip()
        address = page.xpath('//strong[contains(text(), "mail")]/parent::p/text()')[1].replace(':', '').strip()
        phone = page.xpath('//strong[contains(text(), "phone")]/parent::p/text()')[1].split()[1]

        p = Person(primary_org='legislature', name=name, district='Caledon', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.image = page.xpath('//h2[contains(text(), "About me")]/img/@src')[0]
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        return p
