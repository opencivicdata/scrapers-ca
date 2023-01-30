from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.villagesenneville.qc.ca/fr/7/conseil-municipal"


class SennevillePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//section[@class="block text"][./header/h2][position() > 1]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role_and_district, name = councillor.xpath(".//h2/text()")[0].split("-")
            role, district = role_and_district.split(" ", 1)
            if role == "Maire":
                district = "Senneville"
            email = self.get_email(councillor)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath(".//img/@src")[0]
            p.add_contact("email", email)
            yield p
