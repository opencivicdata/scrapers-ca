from utils import CanadianScraper, CanadianPerson as Person

COUNCIL_PAGE = 'http://www.hamilton.ca/council-committee/mayor-council/city-councillors'


class HamiltonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_url = page.xpath('//section/h3[contains(., "Mayor\'s Office")]/a/@href')[0]
        yield self.mayor_data(mayor_url)

        councillors = page.xpath('//div[contains(@class, "menu-name-menu-service-structure")]/li/a')
        assert len(councillors), 'No councillors found'
        for a in councillors:
            yield self.councillor_data(a.attrib['href'])

    def councillor_data(self, url):
        page = self.lxmlize(url)

        district = page.xpath('//h1[contains(., "Ward")]/text()')[0]
        name = page.xpath('//div[@id="wb-pri"]//div[contains(@class, "coh-column third")]/p/strong/text()')[0]
        info_node = page.xpath('//div[@id="wb-pri"]')[0]
        phone = self.get_phone(info_node, area_codes=[289, 365, 905])
        email = self.get_email(info_node)
        photo_url = info_node.xpath('.//img/@src')  # can be empty

        p = Person(primary_org='legislature', name=name, district=district, role='Councillor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)

        if phone:
            p.add_contact('voice', phone, 'legislature')
        if photo_url:
            p.image = photo_url[0]

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath('//h1[contains(., "Mayor")]/text()')[0].split('-')[1].replace('Mayor', '')

        info_node = page.xpath('//div[@id="wb-pri"]')[0]
        phone = self.get_phone(info_node, area_codes=[289, 365, 905])
        email = self.get_email(info_node)
        photo_url = info_node.xpath('.//img/@src')[0]

        p = Person(primary_org='legislature', name=name, district='Hamilton', role='Mayor')
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact('email', email)
        p.add_contact('voice', phone, 'legislature')
        p.image = photo_url

        return p
