from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.richmondhill.ca/en/our-services/Mayor-and-Council.aspx"


class RichmondHillPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        url = page.xpath('//h3[contains(text(), "Mayor")]/following-sibling::p//@href')[0]
        yield self.process(url, "Richmond Hill", "Mayor")

        urls = page.xpath('//h3[contains(text(), "Regional and Local Councillors")]/following-sibling::p[1]//@href')
        assert len(urls), "No regional councillors found"
        for index, url in enumerate(urls, 1):
            yield self.process(url, f"Richmond Hill (seat {index})", "Regional Councillor")

        councillors = page.xpath('//h3[text()="Local Councillors"]/following-sibling::p')
        assert len(councillors), "No councillors found"
        for p in councillors:
            if " - " in p.text_content():
                yield self.process(p.xpath(".//@href")[0], p.text_content().split(" - ", 1)[0], "Councillor")

    def process(self, url, district, role):
        div = self.lxmlize(url).xpath('//div[@id="printAreaContent"]')[0]

        name = div.xpath(".//h2/text()")[0]

        p = Person(primary_org="legislature", name=name, district=district, role=role)
        p.add_contact("email", self.get_email(div))
        p.add_contact("voice", self.get_phone(div, area_codes=[905]), "legislature")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        return p
