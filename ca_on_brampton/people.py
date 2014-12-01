from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx'
MAYOR_PAGE = 'http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx'


class BramptonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillor_divs = page.xpath('//div[@class="councillorCard"]')
        for councillor_div in councillor_divs:
            yield self.councillor_data(councillor_div)

        mayor_page = self.lxmlize(MAYOR_PAGE)
        yield self.mayor_data(mayor_page)


    def councillor_data(self, html):
        role = html.xpath('./div[@class="councillorInfo"]/a/text()[1]')[0]
        name = html.xpath('./div[@class="councillorInfo"]/a/text()[2]')[0]
        email = html.xpath('./div[@class="emailInfo"]//text()')[0]
        district, phone = html.xpath('./div[@class="wardInfo"]/text()')
        photo = html.xpath('.//@src[1]')[0]

        p = Person(primary_org='legislature', name=name, district=district, role=role)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo

        return p


    def mayor_data(self, page):
        # Strip the word "mayor" from the beginning of the photo lavel
        name = page.xpath('string(//img[@class="mayorsPic"]/@alt)').replace('Mayor ', '')  # can be empty
        photo_url = page.xpath('string(//img[@class="mayorsPic"]/@src)')  # can be empty

        if 'Linda Jeffrey' in page.xpath('string(//div[@class="rich-text-Content"])'):
            name = 'Linda Jeffrey'

        email = page.xpath('//div[@class="rich-text-Content"]//a/text()[contains(.,"@")]')[0]
        phone = page.xpath('//div[@class="rich-text-Content"]//text()[contains(.,"905.")]')[0]

        p = Person(primary_org='legislature', name=name, district='Brampton', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo_url
        return p
