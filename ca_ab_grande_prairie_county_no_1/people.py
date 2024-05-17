from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.countygp.ab.ca/en/county-government/council.aspx"


class GrandePrairieCountyNo1PersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(@class, "fbg-row lmRow ui-sortable")]')

        # the first two matching containers have no councillor
        councillors = councillors[3:]

        assert len(councillors), "No councillors found"
        role = "Councillor"
        for councillor in councillors:
            name = councillor.xpath('.//div[@class="lb-imageBox_header {headColor}"]')[0].text_content()
            if "Reeve" in name:
                name = name.split("Reeve")[1].strip()
            district = councillor.xpath(".//h3|.//h2")[0].text_content()

            if district == "Division 5":
                # district 5's councillor is the Reeve
                p = Person(primary_org="legislature", name=name, district=district, role="Reeve")
            elif district == "Division 7":
                # district 7's councillor is the Deputy Reeve
                p = Person(primary_org="legislature", name=name, district=district, role="Deputy Reeve")
            else:
                p = Person(primary_org="legislature", name=name, district=district, role=role)

            p.add_source(COUNCIL_PAGE)
            p.image = councillor.xpath(".//img/@src")[0]

            yield p
