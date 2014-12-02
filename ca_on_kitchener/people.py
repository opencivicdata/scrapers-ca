from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.kitchener.ca/en/insidecityhall/WhoIsMyCouncillor.asp'
MAYOR_PAGE = 'http://www.kitchener.ca/en/insidecityhall/MayorSLandingPage.asp'


class KitchenerPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillor_nodes = page.xpath('//div[@id="printArea"]//li')

        for node in councillor_nodes:
            councillor_url = node.xpath('./a/@href')[0]
            ward = node.xpath('./strong//text()')[0].split('-')[0]
            yield self.councillor_data(councillor_url, ward)

        yield self.mayor_data(MAYOR_PAGE)

    def councillor_data(self, url, ward):
        page = self.lxmlize(url)

        infobox_node = page.xpath('//div[@id="printArea"]')[0]
        name = infobox_node.xpath('.//h1[1]')[0].text_content()[len('Councillor'):]

        contact_node = infobox_node.xpath('.//p[contains(text(), "Coun.")]')[0]
        email = self.get_email(contact_node)

        photo_url_rel = page.xpath('//div[@id="sideBar"]//img/@src')[0]
        photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

        p = Person(primary_org='legislature', name=name, district=ward, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        if email:
            p.add_contact('email', email)
        p.image = photo_url

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        infobox_node = page.xpath('//div[@id="printArea"]')[0]
        name = infobox_node.xpath('.//h1')[0][6:]  # strip 'Mayor' prefix

        photo_url_rel = page.xpath('//div[@id="sideBar"]//img/@src')[0]
        photo_url = urljoin(COUNCIL_PAGE, photo_url_rel)

        p = Person(primary_org='legislature', name=name, district='Kitchener', role='Mayor')
        p.add_source(url)
        p.image = photo_url

        return p
