from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.vernon.ca/government-services/mayor-council"


class VernonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        rows = page.xpath('//div[contains(@class,"view-id-mayor_and_council")]//div[contains(@class,"views-row")]')
        assert rows, "No council member rows found"
        seat = 0
        for row in rows:
            name_texts = row.xpath(".//h3/text()")
            name = name_texts[0].strip() if name_texts else ""
            role_texts = row.xpath(".//h4/text()")
            role_text = role_texts[0].strip() if role_texts else ""
            if not name:
                continue
            if "Mayor" in role_text:
                role, district = "Mayor", "Vernon"
            else:
                seat += 1
                role, district = "Councillor", f"Vernon (seat {seat})"
            email = self.get_email(row, error=False)
            phone = self.get_phone(row, area_codes=[250], error=False)
            image = row.xpath(".//img/@src")
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
