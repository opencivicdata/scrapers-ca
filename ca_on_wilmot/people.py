import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.wilmot.ca/township-office/council/"


class WilmotPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Collapsible sections; trigger link text is "Mayor Natasha Salonen"
        # or "Ward 1 Councillor Stewart Cressman"
        councillors = page.xpath(
            '//a[contains(@href, "#collapse_")][contains(., "Mayor") or contains(., "Councillor")]'
        )
        if not councillors:
            councillors = page.xpath('//a[contains(., "Mayor") or contains(., "Councillor")]')
        assert len(councillors), "No councillors found"
        count = 0
        for councillor in councillors:
            heading = councillor.text_content().strip()
            match = re.match(r"(Mayor|(?:Ward \d+ )?Councillor)\s+(.+)", heading)
            if not match:
                continue
            role_text = match.group(1).strip()
            name = match.group(2).strip()

            if "Councillor" in role_text and role_text != "Councillor":
                district = role_text.split(" Councillor")[0]
                role = "Councillor"
            elif role_text == "Mayor":
                district = "Wilmot"
                role = "Mayor"
            else:
                district = "Wilmot"
                role = role_text

            collapse_id = councillor.get("href").lstrip("#")
            panel = page.xpath(f'//div[@id="{collapse_id}"]')
            panel = panel[0] if panel else councillor.getparent()

            phone = self.get_phone(panel, area_codes=[519, 226, 548], error=False)
            email = self.get_email(panel, error=False)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            count += 1
            yield p

        assert count, "No councillors found"
