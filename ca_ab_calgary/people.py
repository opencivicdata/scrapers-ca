from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.calgary.ca/council/councillors-and-wards.html"


class CalgaryPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "cui card ")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h3")[0].text_content()
            if "Information site" in name:
                continue
            district = councillor.xpath(".//p")[0].text_content()

            role = "Councillor"

            if "Mayor" in district:
                district = "Calgary"
                role = "Mayor"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            photo_style = councillor.xpath(
                './/div[contains(@class, "background-image  bg-pos-x-center bg-pos-y-center ratio-1x1")]/@style'
            )
            p.image = photo_style[0].split("'")[1]
            p.add_source(COUNCIL_PAGE)
            yield p
