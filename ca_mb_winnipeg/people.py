from utils import CanadianScraper, CanadianPerson as Person

import json
import re
import requests

COUNCIL_PAGE = 'http://winnipeg.ca/council/'


class WinnipegPersonScraper(CanadianScraper):
    def scrape(self):
        # https://winnipeg.ca/council/wards/includes/wards.js
        # var COUNCIL_API = 'https://data.winnipeg.ca/resource/r4tk-7dip.json';
        api_url = 'https://data.winnipeg.ca/resource/r4tk-7dip.json'
        data = json.loads(requests.get(api_url).content)

        page = self.lxmlize(COUNCIL_PAGE, 'utf-8')

        councillors = page.xpath('//div[@class="box"]')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            role = councillor.xpath('.//div[@class="insideboxtitle"]/text()')[0].strip()
            name = councillor.xpath('.//p[@class="insideboxtext"]/text()')[0]
            image = councillor.xpath('.//@src')[0]

            if role == 'Mayor':
                district = 'Winnipeg'

                # https://winnipeg.ca/interhom/mayor/navData.xml
                # <pos1 text="Contact the Mayor" link="/interhom/mayor/contact.asp" />
                url = 'https://winnipeg.ca/interhom/mayor/contact.asp'
                page = self.lxmlize(url)

                email = page.xpath('//i[contains(@class, "fa-envelope")]/following-sibling::strong[1]//@href')[0]
                voice = page.xpath('//span[@itemprop="telephone"]/text()')[0]
                fax = page.xpath('//span[@itemprop="faxNumber"]/text()')[0]
            else:
                district = councillor.xpath('.//p[@class="wardname"]/a/text()')

                url = api_url
                item = next(item for item in data if item['person'] == name)

                email = item['email_link']
                voice = item['phone']
                fax = item['fax']

            p = Person(primary_org='legislature', name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if not image.endswith('nophoto.jpg'):
                p.image = image
            p.add_contact('email', parse_email(email))
            p.add_contact('voice', voice, 'legislature')
            p.add_contact('fax', fax, 'legislature')

            yield p


def parse_email(email):
    return re.search('=([^&]+)', email).group(1) + '@winnipeg.ca'
