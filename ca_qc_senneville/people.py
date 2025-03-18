from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.senneville.ca/municipalite/vie-democratique/conseil-municipal/"


class SennevillePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="wp-block-media-text is-stacked-on-mobile"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role_and_district, name = councillor.xpath(".//h2")[0].text_content().split(" – ")
            if "Maire" in role_and_district:
                role = "Maire"
                district = "Senneville"
            else:
                role, district = role_and_district.split(" ", 1)

            email = self.get_email(councillor)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = councillor.xpath(".//img/@src")[0]
            if not image.startswith("data:"):
                p.image = image
            p.add_contact("email", email)
            yield p
