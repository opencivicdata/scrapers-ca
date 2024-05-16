from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.hamilton.ca/city-council/council-committee/city-council-members/city-councillors"
MAYOR_PAGE = "https://www.hamilton.ca/city-council/council-committee/city-council-members/mayors-office"


class HamiltonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        yield self.mayor_data(MAYOR_PAGE)

        councillors = page.xpath('//div[contains(@class, "image-cta-card")]//@href[1]')
        assert len(councillors), "No councillors found"
        for url in councillors:
            yield self.councillor_data(url)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        district = page.xpath("//h1/text()")[0]
        name = page.xpath('//h2[@class="title"]/text()')[0].split("(")[0].strip()
        info_node = page.xpath(
            '//div[@class="section container-md image--right post-card post-card--large bg--#FFFFFF"]'
        )[0]
        phone = self.get_phone(info_node, area_codes=[289, 365, 905])
        email = self.get_email(info_node)
        photo_url = info_node.xpath(".//img/@src")  # can be empty

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact("email", email)

        if phone:
            p.add_contact("voice", phone, "legislature")
        if photo_url:
            p.image = photo_url[0]

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//h2[@class="title"]/text()')[0]

        info_node = page.xpath(
            '//div[@class="section container-md image--right post-card post-card--large bg--#00578E"]'
        )[0]
        phone = self.get_phone(info_node, area_codes=[289, 365, 905])
        email = self.get_email(info_node)
        photo_url = info_node.xpath(".//img/@src")[0]

        p = Person(primary_org="legislature", name=name, district="Hamilton", role="Mayor")
        p.add_source(MAYOR_PAGE)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.image = photo_url

        return p
