import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.sainte-anne-de-bellevue.qc.ca/fr/199/elus-municipaux"


class SainteAnneDeBellevuePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Councillors are in a table; each row has pairs of (photo td, info td)
        # Info td contains: <h2>role</h2>, <p>name</p>, <p><a href="mailto:...">
        info_tds = page.xpath('//table//td[h2[normalize-space(.)!=""]]')
        assert len(info_tds), "No councillors found"

        for td in info_tds:
            role_text = " ".join(td.xpath(".//h2//text()")).strip()
            if not role_text:
                continue

            name_nodes = td.xpath("./p[not(a)]/text()")
            name = next((t.strip() for t in name_nodes if t.strip()), None)
            if not name:
                continue

            email = self.get_email(td, error=False)

            if "Maire" in role_text:
                district = "Sainte-Anne-de-Bellevue"
                role = "Maire"
            else:
                m = re.search(r"\d+", role_text)
                district = "District {}".format(m[0]) if m else role_text
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            yield p
