from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.lethbridge.ca/council-administration-governance/mayor-and-councillors/councillors-office"
MAYOR_PAGE = "https://www.lethbridge.ca/council-administration-governance/mayor-and-councillors/mayors-office"


class LethbridgePersonScraper(CanadianScraper):
    def scrape(self):
        def councillor_scraper(self, url, seat_number):
            page = self.lxmlize(url)
            name = page.xpath('//h1[contains(@class, "heading main base-heading")]')[0].text_content().split(",")[0]

            p = Person(
                primary_org="legislature",
                name=name,
                district="Lethbridge (seat {})".format(seat_number + 1),
                role="Councillor",
            )

            p.image = page.xpath('//span[contains(@class, "img-right")]/img/@src[1]')[0]
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            return p

        def mayor_scraper(self):
            page = self.lxmlize(MAYOR_PAGE)
            paragraph = page.xpath("//p[1]")[0].text_content().split()
            name = " ".join([paragraph[0], paragraph[1]])

            p = Person(primary_org="legislature", name=name, district="Lethbridge", role="Mayor")
            p.image = page.xpath("//img/@src")[0]
            p.add_source(MAYOR_PAGE)

            return p

        yield mayor_scraper(self)
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "inner ")]/a[@href]')
        for seat_number, councillor in enumerate(councillors):
            name = councillor.xpath(".//span")[0].text_content()
            if "Vacant" in name:
                continue
            url = councillor.xpath("./@href")[0]
            yield councillor_scraper(self, url, seat_number)
