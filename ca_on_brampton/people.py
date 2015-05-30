from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.brampton.ca/en/City-Hall/CouncilOffice/Pages/Welcome.aspx'
MAYOR_PAGE = 'http://www.brampton.ca/EN/City-Hall/Office-Mayor/Pages/Welcome.aspx'
MAYOR_CONTACT_PAGE = 'http://www.brampton.ca/EN/City-Hall/Mayor-Office/Pages/Contact-Us.aspx'


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
        email = self.get_email(html, './div[@class="emailInfo"]')
        district, phone = html.xpath('./div[@class="wardInfo"]/text()')
        photo = html.xpath('.//@src[1]')[0]

        p = Person(primary_org='legislature', name=name, district=district, role=role)
        p.add_source(COUNCIL_PAGE)
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('email', email)
        p.image = photo

        return p

    def mayor_data(self, page):
        name = page.xpath('//div[@id="MayorsName"]/h1')[0].text_content().split('Mayor')[1]

        contact_page = self.lxmlize(MAYOR_CONTACT_PAGE)
        address = ' '.join(contact_page.xpath('//div[@class="col-sm-6"][1]/p/text()'))
        contact_info = contact_page.xpath('//div[@class="col-sm-6"][2]/p')[0]
        email = self.get_email(contact_info)

        phone = contact_info.xpath('./text()')[0]
        fax = contact_info.xpath('./text()')[1]

        twitter = contact_info.xpath('./a[contains(@href, "twitter")]/@href')[0]
        facebook = contact_info.xpath('./a[contains(@href, "facebook")]/@href')[0]

        p = Person(primary_org='legislature', name=name, district='Brampton', role='Mayor')
        p.add_source(MAYOR_PAGE)
        p.add_source(MAYOR_CONTACT_PAGE)
        p.add_contact('address', address, 'legislature')
        p.add_contact('voice', phone, 'legislature')
        p.add_contact('fax', fax, 'legislature')
        p.add_contact('email', email)
        p.add_link(twitter)
        p.add_link(facebook)

        return p
