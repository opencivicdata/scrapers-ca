from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.saanich.ca/EN/main/local-government/mayor-council/meet-your-council.html"


class SaanichPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "entry")]')[0].xpath(".//@href")
        assert len(councillors), "No councillors found"
        for url in councillors:
            if "@" in url:
                continue

            page = self.lxmlize(url)
            main = page.xpath('//main[@id="content"]')[0]

            name = main.xpath(".//h1//text()")[0]

            if "Mayor" in main.text_content():
                name = name.replace("Mayor ", "")
                role = "Mayor"
                district = "Saanich"
            else:
                role = "Councillor"
                district = f"Saanich (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = page.xpath(".//@src")[0]
            p.add_contact("voice", self.get_phone(page, area_codes=[250]), "legislature")
            p.add_contact("email", self.get_email(page.xpath('//main[@id="content"]')[0]))
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            yield p
