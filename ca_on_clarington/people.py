import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.clarington.net/town-hall/mayor-and-council/meet-your-councillors/"
MAYOR_PAGE = "https://www.clarington.net/town-hall/mayor-and-council/mayor/"


class ClaringtonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Collapsible sections; trigger link text is "Name - Role Wards X & Y"
        # e.g. "Granville Anderson - Regional Councillor Wards 1 & 2"
        councillors = page.xpath('//a[contains(@href, "#collapse_") and contains(., " - ")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            heading = councillor.text_content().strip()
            name, role_district = heading.split(" - ", 1)
            name = name.strip()
            match = re.match(r"((?:Regional )?Councillor)\s+(.+)", role_district.strip())
            if not match:
                continue
            role = match.group(1)
            district = match.group(2).strip()

            collapse_id = councillor.get("href").lstrip("#")
            panel = page.xpath(f'//div[@id="{collapse_id}"]')
            if not panel:
                continue
            panel = panel[0]

            email = self.get_email(panel)
            photo = panel.xpath(".//img/@src")
            photo_url = photo[0] if photo else None

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            yield p

        mayor_page = self.lxmlize(MAYOR_PAGE)
        # The mayor's name appears as the first word(s) in the first bio paragraph
        bio = mayor_page.xpath('//h1[contains(., "Mayor")]/following-sibling::p[1]/text()')
        name_match = re.match(r"(\w+ \w+) is serving", bio[0].strip()) if bio else None
        name = (
            name_match.group(1)
            if name_match
            else mayor_page.xpath('//h2[contains(., "Mayor")]')[0]
            .text_content()
            .split("Mayor")[1]
            .strip()
            .split("'")[0]
            .strip()
        )
        email = self.get_email(mayor_page)
        photo = mayor_page.xpath('//img[contains(@src, "/media/")]/@src')
        photo_url = photo[0] if photo else None

        p = Person(primary_org="legislature", name=name, district="Clarington", role="Mayor", image=photo_url)
        p.add_contact("email", email)
        p.add_source(MAYOR_PAGE)
        yield p
