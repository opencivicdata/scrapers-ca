from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//p[a[contains(@href, "@")]]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            role = councillor.xpath("./preceding-sibling::h2[1]/text()")[0]

            if role == "Maire":
                district = "Sainte-Anne-de-Bellevue"
            else:
                district = "District " + role.split()[2]
                role = "Conseiller"

            councillor = councillor.text_content().split()

            name = " ".join(councillor[:2])
            email = councillor[3]
            email = email.replace("Président", "")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)

            yield p
