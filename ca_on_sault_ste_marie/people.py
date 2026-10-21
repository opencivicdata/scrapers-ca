import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://saultstemarie.ca/Government/City-Council.aspx"
MAYOR_PAGE = "https://saultstemarie.ca/government/city-council/office-of-the-mayor/"


class SaultSteMariePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        seat_numbers = defaultdict(int)

        # Councillors are listed inline as h3 elements: "Ward X - Councillor Name"
        councillor_headings = page.xpath('//h3[contains(., "Councillor")]')
        assert len(councillor_headings), "No councillors found"

        # Scrape mayor from dedicated page
        mayor_page = self.lxmlize(MAYOR_PAGE)
        mayor_h2 = mayor_page.xpath('//h2[contains(text(), "Mayor")]')
        if mayor_h2:
            mayor_title = mayor_h2[0].text_content().strip()
            # e.g. "About Mayor Matthew Shoemaker"
            mayor_name = re.sub(r".*\bMayor\s+", "", mayor_title).strip()
        else:
            mayor_name = mayor_page.xpath("//h1")[0].text_content().replace("Office of the Mayor", "").strip()
        mayor_phone = self.get_phone(mayor_page, error=False)
        mayor_email = self.get_email(mayor_page, error=False)
        mayor_image_nodes = mayor_page.xpath('//img[contains(@src, "Mayor")]/@src')
        mayor_image = mayor_image_nodes[0] if mayor_image_nodes else None

        p = Person(primary_org="legislature", name=mayor_name, district="Sault Ste. Marie", role="Mayor")
        if mayor_image:
            p.image = mayor_image
        if mayor_email:
            p.add_contact("email", mayor_email)
        if mayor_phone:
            p.add_contact("voice", mayor_phone, "legislature")
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_PAGE)
        yield p

        for heading in councillor_headings:
            title = heading.text_content().strip()
            # Format: "Ward X - Councillor First Last"
            m = re.match(r"(Ward \d+)\s*-\s*Councillor\s+(.+)", title)
            if not m:
                continue
            area = m.group(1)
            name = m.group(2).strip()
            seat_numbers[area] += 1
            district = f"{area} (seat {seat_numbers[area]})"

            # Contact info is in the sibling p tags after the h3
            # Find phone and email from following siblings
            parent = heading.getparent()
            phone = self.get_phone(parent, error=False)
            email = self.get_email(parent, error=False)
            image_nodes = parent.xpath(".//img/@src")
            image = image_nodes[0] if image_nodes else None

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            if image:
                p.image = image
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            yield p
