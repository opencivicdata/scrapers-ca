import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.belleville.ca/en/city-hall/councillors.aspx"
MAYOR_PAGE = "https://www.belleville.ca/en/city-hall/mayors-office.aspx"


class BellevillePersonScraper(CanadianScraper):
    seat_numbers = defaultdict(int)

    def get_belleville_phone(self, node):
        phone = self.get_phone(node)
        if phone.startswith("//"):
            phone = phone.lstrip("/")
        return phone.replace(",", " x")

    def scrape(self):
        page = self.lxmlize(MAYOR_PAGE)

        name = page.xpath('//div[contains(@class, "text base-text")]/p[contains(text(), " is the ")]/text()')[0].split(
            " is the "
        )[0]
        phone = self.get_belleville_phone(page)
        email = self.get_email(page)
        image = page.xpath('//img[contains(@src, "/media/") and not(contains(@src, "logo"))]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Belleville", role="Mayor")
        p.add_source(MAYOR_PAGE)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("email", email)
        p.image = image

        yield p

        page = self.lxmlize(COUNCIL_PAGE)
        wards = page.xpath('//h2[contains(text(), "Ward")]')
        assert len(wards), "No wards found"
        for ward in wards:
            ward_name = ward.text.strip()
            accordions = ward.xpath(
                './following-sibling::div[contains(@class, "accordion")][1]//a[starts-with(@href, "#collapse_")]'
            )
            for anchor in accordions:
                self.seat_numbers[ward_name] += 1
                district = f"{ward_name} (seat {self.seat_numbers[ward_name]})"
                councillor_name = anchor.text_content().strip()
                collapse_id = anchor.get("href").lstrip("#")
                content = page.xpath(f'//div[@id="{collapse_id}"]')
                if not content:
                    continue
                content = content[0]
                image_nodes = content.xpath(".//img/@src")
                image = image_nodes[0] if image_nodes else None
                phone = self.get_belleville_phone(content)
                email = self.get_email(content, error=False)

                p = Person(primary_org="legislature", name=councillor_name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)
                if phone:
                    p.add_contact("voice", phone, "legislature")
                if email:
                    p.add_contact("email", email)
                if image:
                    p.image = image

                yield p
                if self.seat_numbers[ward_name] >= 6:  # Assigning councillors to correct Ward
                    break
