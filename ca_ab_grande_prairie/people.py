from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://cityofgp.com/city-government/mayor-city-council/council-members"


class GrandePrairiePersonScraper(CanadianScraper):
    def scrape(self):
        seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "council-bios")]//div[@class="views-row"]')

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, name = councillor.xpath(".//h3")[0].text_content().split(" ", 1)
            if role == "Councillor":
                district = f"Grande Prairie (seat {seat_number})"
                seat_number += 1
            else:
                district = " Grande Prairie"
            email = self.get_email(councillor)
            phone = self.get_phone(councillor)
            image = councillor.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)

            yield p
