from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://ville.montreal-est.qc.ca/vie-democratique/conseil-municipal/"


class MontrealEstPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath(
            '//div[contains (@class, "membreimg text-center membres-conseil")]//div//div[@class="col-lg-6"]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="bg-trans-gris"]/span/text()')[0]

            if "Maire" in name or "Mairesse" in name:
                name = name.split(" ", 2)[:2]
                name = " ".join(name)
                district = "Montréal-Est"
                role = "Maire"
            else:
                name, district = name.split(" ", 2)[:2], "District " + name.split(" ")[-1]
                name = " ".join(name)
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath(".//div[not(@id)]/img//@src")[0]
            p.add_contact("email", self.get_email(councillor))
            p.add_source(COUNCIL_PAGE)
            yield p
