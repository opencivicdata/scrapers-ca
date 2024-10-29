import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="block text"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="content-writable"]//strong/text()')[0]
            district = councillor.xpath(".//h2/text()")[0]

            if "Maire" in district:
                district = "Sainte-Anne-de-Bellevue"
                role = "Maire"
            else:
                district = "District {}".format(re.search(r"\d+", district)[0])
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath(".//@src")[0]
            p.add_contact("email", self.get_email(councillor))
            yield p
