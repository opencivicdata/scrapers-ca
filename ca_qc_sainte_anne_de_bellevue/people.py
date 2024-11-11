import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//p[a[contains(@href, "@")]]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name = councillor.text_content().split(" |", 1)[0]
            district = councillor.xpath("./preceding-sibling::h2[1]/text()")[0]

            if "Maire" in district:
                district = "Sainte-Anne-de-Bellevue"
                role = "Maire"
            else:
                district = "District {}".format(re.search(r"\d+", district)[0])
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.add_contact("email", self.get_email(councillor))
            yield p
