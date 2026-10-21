import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.alma.qc.ca/conseil-municipal-2/"


class AlmaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        headings = page.xpath("//h4[normalize-space()]")
        assert len(headings) >= 9, "Expected at least 9 council member headings"

        seen = set()
        for heading in headings:
            container = heading.xpath('./ancestor::div[contains(@class, "col")][1]')[0]
            name = " ".join(heading.text_content().split())
            name = re.sub(r"^(?:Madame|Monsieur)\s+", "", name)
            if name in seen:
                continue
            seen.add(name)

            texts = [text.strip() for text in container.xpath(".//text()") if text.strip()]
            district_bits = []
            for text in texts:
                if text.startswith("Carte du district") or text.startswith(("Madame", "Monsieur")):
                    break
                if text.startswith("District") or (
                    district_bits and not text.startswith(("Cellulaire", "Résidence", "Courriel"))
                ):
                    district_bits.append(text)
            if name == "Sylvie Beaumont":
                role = "Maire"
                district = "Alma"
            else:
                role = "Conseiller"
                district_number = re.search(r"#\s*(\d+)", district_bits[0])
                district = f"District {district_number.group(1)}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            email = self.get_email(container, error=False)
            if email:
                p.add_contact("email", email)
            phone = self.get_phone(container, area_codes=[418, 581], error=False)
            if phone:
                p.add_contact("voice", re.sub(r"\s+", " ", phone), "legislature")
            yield p
