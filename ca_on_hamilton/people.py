from __future__ import unicode_literals
from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.hamilton.ca/YourElectedOfficials/WardCouncillors/'


class HamiltonPersonScraper(CanadianScraper):

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        council_node = page.xpath('//span[@id="RadEditorPlaceHolderControl0"]')[0]
        councillor_urls = council_node.xpath('./table[2]//p/a[not(img)]/@href')

        for councillor_url in councillor_urls:
            yield self.councillor_data(councillor_url)

        yield self.mayor_data(council_node.xpath('./table[1]/tbody/tr')[0])

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name, district = page.xpath('//span[@id="_hpcPageTitle"]//text()')[0].split('-')

        info_node = page.xpath('//span[@id="RadEditorPlaceHolderControl0"]')[0]
        phone = self.get_phone(info_node, [289, 365, 905])
        email = self.get_email(info_node)
        photo_url = info_node.xpath('string(.//img/@src)')  # can be empty

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)

        if phone:
            p.add_contact('voice', phone, 'legislature')
        if photo_url:
            p.image = photo_url

        return p

    def mayor_data(self, node):
        name = node.xpath('.//strong')[0][6:]
        phone = node.xpath('.//p[2]/text()[1]')[0]
        email = self.get_email(node)
        photo_url = node.xpath('.//img/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Hamilton', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        p.image = photo_url

        return p
