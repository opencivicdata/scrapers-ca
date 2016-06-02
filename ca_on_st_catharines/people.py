from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.stcatharines.ca/en/governin/MayorCouncil.asp'


class StCatharinesPersonScraper(CanadianScraper):

    def scrape(self):
        # TODO Use https://niagaraopendata.ca/dataset/st-catharines-councilors
        page = self.lxmlize(COUNCIL_PAGE)

        council = page.xpath('//ul[@id="subNav"]/li[@class="withChildren"]/ul/li/a')
        yield self.scrape_mayor(council[0].attrib['href'])

        wards = council[1:]

        for ward in wards:
            url = ward.attrib['href']
            ward_page = self.lxmlize(url)

            district = ward_page.xpath('//div[@class="contentArea"]/div[1]/h1/text()')[0].split('-')[1]
            councillors = ward_page.xpath('//div[@class="contentArea"]/div[1]/h2')
            for councillor in councillors:
                name = councillor.text_content().replace('Coun.', '')

                p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)

                image = councillor.xpath('./following-sibling::p[1]//@src')
                if image:
                    p.image = image[0]

                if councillor.xpath('./following-sibling::p[1]//a'):
                    position = 1
                elif councillor.xpath('./following-sibling::p[2]//a'):
                    position = 2
                else:
                    position = 3
                phone = self.get_phone(councillor.xpath('./following-sibling::p[{}]'.format(position))[0], area_codes=[289, 905])
                email = self.get_email(councillor.xpath('./following-sibling::p[{}]'.format(position))[0])
                address = ' '.join(councillor.xpath('./following-sibling::p[{}]/text()'.format(position + 1)))
                address = address.replace('Mail:', '')

                p.add_contact('address', address, 'legislature')
                p.add_contact('voice', phone, 'legislature')
                p.add_contact('email', email)
                yield p

    def scrape_mayor(self, url):
        mayor_page = self.lxmlize(url)
        mayor_info = mayor_page.xpath('//div[@class="contentArea"]/div[1]')[0]
        name = mayor_info.xpath('./h2/text()')[0].replace('Mayor', '')

        p = Person(primary_org='legislature', name=name, district='St. Catharines', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        p.image = mayor_info.xpath('./h2/img/@src')[0]

        phone = mayor_info.xpath('./p[1]/text()')[1]
        address = ' '.join(mayor_info.xpath('./p[2]/text()'))

        phone = phone.split('or')[0].replace('Phone:', '')
        address = address.replace('Mail:', '')
        email = 'mayorsadministration@stcatharines.ca'

        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)

        return p
