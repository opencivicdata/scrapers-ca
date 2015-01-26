from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.legassembly.sk.ca/mlas/'


class SaskatchewanPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@id="MLAs"]//tr')[1:]
        for councillor in councillors:
            name = councillor.xpath('./td')[0].text_content().split('. ', 1)[1]
            party = councillor.xpath('./td')[1].text
            district = councillor.xpath('./td')[2].text_content()
            url = councillor.xpath('./td[1]/a/@href')[0]
            page = self.lxmlize(url)

            p = Person(primary_org='legislature', name=name, district=district, role='MLA', party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.image = page.xpath('//div[contains(@class, "mla-image-cell")]/img/@src')[0]

            contact = page.xpath('//div[@id="mla-contact"]/div[2]')[0]
            website = contact.xpath('./div[3]/div[3]/div[2]/a')
            if website:
                p.add_link(website[0].text_content())

            p.add_contact('address', ' '.join(contact.xpath('.//div[@class="col-md-4"][2]/div//text()')[1:9]), 'constituency')
            phone_leg = contact.xpath('.//span[@id="MainContent_ContentBottom_Property6"]//text()')[0]
            phone_const = contact.xpath('.//div[@class="col-md-4"]/div[4]/span/span/text()')[0]
            p.add_contact('voice', phone_leg, 'legislature', area_code=306)
            p.add_contact('voice', phone_const, 'constituency', area_code=306)
            email = self.get_email(contact)
            p.add_contact('email', email)

            yield p
