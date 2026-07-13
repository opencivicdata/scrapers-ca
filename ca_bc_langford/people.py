from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://langford.ca/city-hall/council-committees/mayor-council/"


class LangfordPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        bios = page.xpath("//div[@class='bio']")
        assert bios, "No bio cards found"

        seat = 0
        for bio in bios:
            title_els = bio.xpath(".//div[contains(@class,'bio-title')]")
            position_els = bio.xpath(".//*[contains(@class,'bio-position')]")
            if not title_els or not position_els:
                continue

            name = title_els[0].text_content().strip()
            position = position_els[0].text_content().strip()

            if not name:
                continue

            if position == "Mayor":
                role = "Mayor"
                district = "Langford"
            else:
                seat += 1
                role = "Councillor"
                district = f"Langford (seat {seat})"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            yield p
