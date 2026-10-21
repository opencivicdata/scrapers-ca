from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://saintejulie.ca/conseil-municipal/le-maire-et-les-conseillers-municipaux"


class SainteJuliePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(@class, "fiche__info")][.//h1[contains(@class, "fiche__title")]]')
        assert len(members) == 9, "Expected 9 council members"

        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            name = " ".join(text[0].split())
            if text[1] == "Maire":
                role = "Maire"
                district = "Sainte-Julie"
            else:
                role = "Conseiller"
                district = text[1]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            image = member.xpath('./preceding-sibling::*//img[contains(@alt, "Photo de")]/@src')
            if image:
                p.image = image[0]
            yield p
