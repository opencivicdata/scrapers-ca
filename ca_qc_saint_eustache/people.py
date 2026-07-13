import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.saint-eustache.ca/ville/vie-democratique/conseil-municipal"


class SaintEustachePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        cards = page.xpath('//div[contains(@class,"c-rubric-card")]')
        assert cards, "No c-rubric-card divs found"
        seen = set()
        for card in cards:
            name_h3 = card.xpath('.//h3[contains(@class,"c-rubric-card__title")]')
            if not name_h3:
                continue
            name = name_h3[0].text_content().strip()
            if not name:
                continue
            if name.startswith("Formation sur"):
                continue
            surtitle = card.xpath('.//span[contains(@class,"c-rubric-card__surtitle")]')
            surtitle_text = surtitle[0].text_content().strip() if surtitle else ""
            if "Maire" in surtitle_text and "Conseill" not in surtitle_text:
                role, district = "Mayor", "Saint-Eustache"
            else:
                m = re.search(r"District\s+(\d+)", surtitle_text, re.I)
                if not m:
                    continue
                role, district = "Councillor", f"District {int(m.group(1))}"
            key = (name, role, district)
            if key in seen:
                continue
            seen.add(key)
            email = self.get_email(card, error=False)
            phone_link = card.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = card.xpath(".//img/@src")
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
