from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brantford.ca/your-government/city-council/"
MAYOR_PAGE = "https://www.brantford.ca/your-government/city-council/office-of-the-mayor/"


class BrantfordPersonScraper(CanadianScraper):
    seat_numbers = defaultdict(int)

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Mayor is listed separately
        mayor_page = self.lxmlize(MAYOR_PAGE)
        mayor_name_nodes = mayor_page.xpath("//h1//text()")
        mayor_name = " ".join(mayor_name_nodes).strip() if mayor_name_nodes else ""
        for prefix in ("About Mayor ", "About "):
            if mayor_name.startswith(prefix):
                mayor_name = mayor_name[len(prefix) :]
                break
        if not mayor_name or mayor_name == "Office of the Mayor":
            # h1 is the page title; name is in a paragraph like "About Mayor Kevin Davis"
            about_p = mayor_page.xpath('//p[contains(normalize-space(), "About Mayor ")]')
            if about_p:
                mayor_name = about_p[0].text_content().strip()
                if mayor_name.startswith("About Mayor "):
                    mayor_name = mayor_name[len("About Mayor ") :]

        p = Person(primary_org="legislature", name=mayor_name, district="Brantford", role="Mayor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_PAGE)
        email = self.get_email(mayor_page, error=False)
        if email:
            p.add_contact("email", email)
        phone = self.get_phone(mayor_page, area_codes=[519, 226, 548], error=False)
        if phone:
            p.add_contact("voice", phone, "legislature")
        yield p

        # Councillors: ward sections use h3 headings; each ward has 2 councillors
        wards = page.xpath('//h3[contains(text(), "Ward")]')
        assert len(wards), "No wards found"
        for ward in wards:
            ward_name = ward.text_content().strip()
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

                p = Person(primary_org="legislature", name=councillor_name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)

                phone = self.get_phone(content, area_codes=[519, 226, 548], error=False)
                if phone:
                    p.add_contact("voice", phone, "legislature")
                email = self.get_email(content, error=False)
                if email:
                    p.add_contact("email", email)
                image = content.xpath(".//img/@src")
                if image:
                    p.image = image[0]

                yield p
