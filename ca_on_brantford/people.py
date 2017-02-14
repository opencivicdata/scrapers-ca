from utils import CanadianScraper, CanadianPerson as Person

import re
from collections import defaultdict

COUNCIL_PAGE = 'http://www.brantford.ca/govt/council/members/Pages/default.aspx'


class BrantfordPersonScraper(CanadianScraper):

    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor()

        councillors = page.xpath('//div[@id="centre_content"]//tr')
        assert len(councillors), 'No councillors found'
        for councillor in councillors:
            if 'Position' in councillor.text_content():
                continue

            ward = councillor.xpath('./td')[0].text_content().replace('Councillor', '')
            seat_numbers[ward] += 1
            district = '{} (seat {})'.format(ward, seat_numbers[ward])
            name = councillor.xpath('./td')[1].text_content()
            url = councillor.xpath('./td/a')[0].attrib['href']

            p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            page = self.lxmlize(url)

            content = page.xpath('//div[@id="centre_content"]')[0]
            email = self.get_email(content)
            p.add_contact('email', email)
            p.add_contact('voice', self.get_phone(content, area_codes=[226, 519]), 'legislature')

            p.image = page.xpath('string(//div[@id="centre_content"]//img/@src)')  # can be empty

            if len(page.xpath('//div[@id="centre_content"]//a')) > 2:
                p.add_link(page.xpath('//div[@id="centre_content"]//a')[-1].attrib['href'])
            yield p

    def scrape_mayor(self):
        mayor_url = 'http://mayor.brantford.ca/Pages/default.aspx'
        page = self.lxmlize(mayor_url)
        name = re.findall(r'(?<=Mayor )(.*)(?=\r)', page.xpath('//div[@id="main_content"]/h1/text()')[0])[0]

        p = Person(primary_org='legislature', name=name, district='Brantford', role='Mayor')
        p.add_source(mayor_url)

        contact_url = page.xpath('.//a[contains(text(),"Contact")]/@href')[0]
        page = self.lxmlize(contact_url)
        p.add_source(contact_url)

        address = ' '.join(page.xpath('//div[@id="main_content"]/p/text()'))
        address = re.sub(r'\s{2,}', ' ', address).strip()
        email = self.get_email(page)

        p.add_contact('address', address, 'legislature')
        p.add_contact('email', email)

        return p
