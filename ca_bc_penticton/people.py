from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_URL = "https://www.penticton.ca/city-hall/city-council/meet-your-city-council"


class PentictonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_URL)
        rows = page.xpath('//div[contains(@class,"list-item--simple") and contains(@class,"views-row")]')
        assert rows, "No council member rows found"
        seat = 0
        for row in rows:
            name_a = row.xpath('.//a[contains(@href,"/staff-directory/")]')
            name = name_a[0].text_content().strip() if name_a else ""
            if not name:
                continue
            role_el = row.xpath('.//*[contains(@class,"list-item__field")]//text()')
            role_text = role_el[0].strip() if role_el else ""
            if "Mayor" in role_text:
                role, district = "Mayor", "Penticton"
            else:
                seat += 1
                role, district = "Councillor", f"Penticton (seat {seat})"
            image = []
            if name_a and name_a[0].get("href"):
                href = name_a[0].get("href")
                profile_url = href if href.startswith("http") else f"https://www.penticton.ca{href}"
                try:
                    ppage = self.lxmlize(profile_url)
                    image = ppage.xpath("//article//img/@src")
                except Exception:
                    pass
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_URL)
            if image:
                p.image = image[0]
            yield p
