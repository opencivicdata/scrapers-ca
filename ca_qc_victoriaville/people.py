import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

MEMBERS_URL = "https://victoriaville.ca/conseil-municipal-et-elections/membres-conseil-municipal"


class VictoriavillePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(MEMBERS_URL)
        sections = page.xpath('//section[contains(@class,"module-colonnes")]')
        assert sections, "No council sections found"

        for section in sections:
            h3 = section.xpath(".//h3")
            if not h3:
                continue
            name = h3[0].text_content().strip()

            desc_p = section.xpath(".//p[not(.//a)][normalize-space()]")
            desc_text = desc_p[0].text_content().strip() if desc_p else ""

            if "Maire" in desc_text or "Mayor" in desc_text:
                role = "Mayor"
                district = "Victoriaville"
            else:
                m = re.search(r"\((\d+)\)", desc_text)
                role = "Councillor"
                district = f"District {m.group(1)}" if m else desc_text

            email_links = section.xpath(".//a[contains(@href,'mailto:')]/@href")
            email = email_links[0].replace("mailto:", "") if email_links else None
            phone_link = section.xpath('.//a[starts-with(@href,"tel:")]')
            phone = phone_link[0].text_content().strip() if phone_link else None
            image = section.xpath(".//figure//img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(MEMBERS_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
