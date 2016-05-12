from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.calgary.ca/General/Pages/Calgary-City-Council.aspx'
MAYOR_PAGE = 'http://calgarymayor.ca/contact'


class CalgaryPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        nodes = page.xpath('//div[contains(@class,"cocis-has-caption")]')[1:]
        for node in nodes:
            url = urljoin(COUNCIL_PAGE, node.xpath('.//a[1]/@href')[0])
            name = node.xpath('.//a//text()')[0]
            ward = ' '.join(node.xpath('.//strong//text()')[0].split()[:-1])
            yield self.councillor_data(url, name, ward)

        # mayor_node = page.xpath('//div[contains(@class, "cocis-image-panel")]')[0]
        photo_url = urljoin(COUNCIL_PAGE, mayor_node.xpath('.//img/@src')[0])
        name = mayor_node.xpath('.//a//text()')[0]
        mayor_page = self.lxmlize(MAYOR_PAGE)
        # Email behind mailhide
        # email = self.get_email(mayor_page)
        phone = self.get_phone(mayor_page, area_codes=[403])
        m = Person(primary_org='legislature', name=name, district='Calgary', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(MAYOR_PAGE)
        m.add_contact('voice', phone, 'legislature')
        m.image = photo_url
        yield m

    def councillor_data(self, url, name, ward):
        page = self.lxmlize(url)
        photo_url_rel = page.xpath('string(//div[@id="contactInfo"]//img[1]/@src)')  # can be empty
        photo_url = urljoin(url, photo_url_rel) if photo_url_rel else None
        email = self.get_email(page, error=False)
        phone = page.xpath('string(//p[contains(./strong, "Phone")]/text())').strip()  # can be empty

        p = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        if email:
            p.add_contact('email', email)
        if phone:
            p.add_contact('voice', phone, 'legislature')
        if photo_url:
            p.image = photo_url

        return p
