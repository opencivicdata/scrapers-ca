from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.campbellriver.ca/government/city-council"


class CampbellRiverPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        items = page.xpath('//div[contains(@class,"field--name-field-row-content")]//div[@class="field__item"][.//h3]')
        assert items, "No council member items found"
        seat = 0
        for item in items:
            name = " ".join(item.xpath(".//h3//text()")).strip()
            if not name:
                continue
            p_text = " ".join(item.xpath(".//p//text()")).strip()
            if "Elected Mayor:" in p_text:
                role, district = "Mayor", "Campbell River"
            else:
                seat += 1
                role, district = "Councillor", f"Campbell River (seat {seat})"
            email = self.get_email(item, error=False)
            phone = self.get_phone(item, area_codes=[250], error=False)
            image = item.xpath(".//img/@src")
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
