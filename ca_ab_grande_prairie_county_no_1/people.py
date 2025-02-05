from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.countygp.ab.ca/en/county-government/council.aspx"


class GrandePrairieCountyNo1PersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "fbg-row lmRow ui-sortable")]')

        councillors = councillors[4:]

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="lb-imageBox_header {headColor}"]')[0].text_content()
            if "Reeve" in name:
                name = name.split("Reeve")[1].strip()
            district = councillor.xpath(".//h3|.//h2")[0].text_content()

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")

            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath(".//img/@src")[0]

            yield p
