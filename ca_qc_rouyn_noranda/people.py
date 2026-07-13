import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.rouyn-noranda.ca/ville/vie-democratique/conseil-municipal"


class RouynNorandaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        # Page uses h2.rubric__title for each member's name; role/district in sibling elements
        h2_nodes = page.xpath('//h2[@class="rubric__title"]')
        assert h2_nodes, "No rubric__title h2 found"
        for h2 in h2_nodes:
            name = h2.text_content().strip()
            if not name:
                continue
            parent = h2.getparent()
            # Collect text of sibling elements (role/district label)
            sibling_texts = [
                el.text_content().strip()
                for el in parent.xpath("./*")
                if el.text_content().strip() and el.text_content().strip() != name
            ]
            role_text = sibling_texts[0] if sibling_texts else ""
            if "Mairie" in role_text:
                role, district = "Mayor", "Rouyn-Noranda"
            elif re.search(r"District\s+\d+", role_text):
                m = re.search(r"District\s+(\d+)", role_text)
                role, district = "Councillor", f"District {int(m.group(1))}"
            else:
                continue  # Skip non-person entries
            email_a = parent.xpath('.//a[starts-with(@href,"mailto:")]')
            email = email_a[0].get("href").replace("mailto:", "") if email_a else None
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            yield p
