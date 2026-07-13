from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.mission.ca/council-government/mayor-council"


class MissionPersonScraper(CanadianScraper):
    def scrape(self):
        _UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        page = self.lxmlize(COUNCIL_URL, user_agent=_UA)
        rows = page.xpath('//div[contains(@class,"view-id-mayor_council")]//div[@class="views-row"]')
        assert rows, "No council member rows found"
        seat = 0
        for row in rows:
            title_texts = row.xpath(".//h3//text()")
            title = " ".join(t.strip() for t in title_texts if t.strip())
            if not title:
                continue
            parts = title.rsplit(", ", 1)
            name = parts[0].strip()
            role_text = parts[1].strip() if len(parts) > 1 else ""
            if "Mayor" in role_text:
                role, district = "Mayor", "Mission"
            else:
                seat += 1
                role, district = "Councillor", f"Mission (seat {seat})"
            email = self.get_email(row, error=False)
            phone = self.get_phone(row, area_codes=[604, 778], error=False)
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
