from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.oshawa.ca/city-hall/city-council-members.asp"


class OshawaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath("//table//td[*]")

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district, role, name = councillor.xpath("./p[1]/text()")
            role = role.strip()

            if district == "City of Oshawa":
                district = "Oshawa"

            if role == "City Councillor":
                role = "Councillor"
            elif role == "Regional & City Councillor":
                role = "Regional Councillor"

            photo_url = councillor.xpath("./p/img/@src")[0]
            phone = self.get_phone(councillor.xpath('./p[contains(.//text(), "Phone")]')[0], area_codes=[905])

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", self.get_email(councillor))
            yield p
