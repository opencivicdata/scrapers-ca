from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

from six.moves.urllib.parse import urljoin

COUNCIL_PAGE = 'http://www.victoria.ca/EN/main/city/mayor-council-committees/councillors.html'


class VictoriaPersonScraper(CanadianScraper):

    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        nodes = page.xpath('//div[@id="content"]/ul/li')
        for node in nodes:
            url = urljoin(COUNCIL_PAGE, node.xpath('./a/@href')[0])
            name = node.xpath('./a//text()')[0]
            district = 'Victoria (seat %d)' % councillor_seat_number
            councillor_seat_number += 1
            yield self.councillor_data(url, name, district)

        mayor_node = page.xpath('(//div[@id="section-navigation-middle"]/ul/li/ul/li/a)[1]')[0]
        mayor_url = urljoin(COUNCIL_PAGE, mayor_node.xpath('./@href')[0])
        mayor_name = mayor_node.xpath('.//text()')[0]
        yield self.mayor_data(mayor_url, mayor_name)

    def councillor_data(self, url, name, district):
        page = self.lxmlize(url)
        email = self.get_email(page)
        phone_str = page.xpath('//div[@id="content"]//strong[1]/following-sibling::text()[contains(., "Phone")]')[0]
        phone = phone_str.split(':')[1]
        photo_url = urljoin(url, page.xpath('//div[@id="content"]//img[1]/@src')[0])

        # TODO: should district be "Nieghborhood Liaison"?
        m = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)
        m.add_contact('email', email)
        m.add_contact('voice', phone, 'legislature')
        m.image = photo_url
        return m

    def mayor_data(self, url, name):
        page = self.lxmlize(url)
        email = self.get_email(page)
        phone_str = page.xpath('//div[@id="content"]//strong[1]/following-sibling::text()[contains(., "phone")]')[0]
        phone = phone_str.split(':')[1]
        photo_url = urljoin(url, page.xpath('//div[@id="content"]//img[1]/@src')[0])

        # TODO: should district be "Nieghborhood Liaison"?
        m = Person(primary_org='legislature', name=name, district='Victoria', role='Mayor')
        m.add_source(COUNCIL_PAGE)
        m.add_source(url)
        m.add_contact('email', email)
        m.add_contact('voice', phone, 'legislature')
        m.image = photo_url
        return m
