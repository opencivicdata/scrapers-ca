from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ville.montreal-est.qc.ca/vie-democratique/conseil-municipal/"


class MontrealEstPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath(
            '//div[contains (@class, "membreimg text-center membres-conseil")]//div//div[@class="col-lg-6"]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name, role_district = councillor.xpath('.//div[@class="bg-trans-gris"]/span/text()')[0].split(" – ", 1)

            if "Maire" in role_district or "Mairesse" in role_district:
                district = "Montréal-Est"
                role = "Maire"
            else:
                district = f"District {role_district[-1]}"
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name.strip(), district=district, role=role)
            p.image = councillor.xpath(".//div[not(@id)]/img//@src")[0]
            p.add_contact("email", self.get_email(councillor))
            p.add_source(COUNCIL_PAGE)
            yield p
