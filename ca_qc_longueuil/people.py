import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://longueuil.quebec/fr/services/elus"
MAYOR_PAGE = "https://longueuil.quebec/fr/mairesse"


class LongueuilPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, "utf-8")

        yield self.scrape_mayor()

        trs = page.xpath("//tbody/tr")
        assert len(trs), "No councillors found"
        seat_number = 1
        for tr in trs:
            if tr.xpath('./td[1]//strong[contains(., "ARRONDISSEMENT")]'):
                continue

            detail_url = tr.xpath(".//@href")[0] if tr.xpath(".//@href") else None
            if not detail_url:
                continue

            district_parts = tr.xpath('.//p[strong[contains(., "District")]]/text()')
            district = "".join(district_parts).strip().replace("\xa0", "")
            district = re.sub(r"\s*[\u2010\u2011\u2012\u2013\u2014\u2015]\s*", "-", district)
            if "Greenfield Park" in district:
                district = f"Greenfield Park (siège {seat_number})"
                seat_number += 1

            district = {
                "Fatima Parcours-du-Cerf": "Fatima-Parcours-du-Cerf",
                "LeMoyne-de Jacques-Cartier": "LeMoyne-Jacques-Cartier",
                "Vieux-Saint-Hubert-de la Savane": "Vieux-Saint-Hubert-la Savane",
            }.get(district, district)

            detail_page = self.lxmlize(detail_url, "utf-8")

            name = detail_page.xpath("//h1/text()")[0]
            photo = detail_page.xpath("//img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)
            if photo:
                p.image = photo[0]
            p.add_contact("email", self.get_email(detail_page))
            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)
        name = page.xpath("//h1[not(@class)]/text()")[0]
        img = page.xpath(f'//img[contains(./@alt, "{name}")]/@src')[0]
        p = Person(primary_org="legislature", name=name, district="Longueuil", role="Maire")
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_PAGE)
        p.image = img
        p.add_contact("email", self.get_email(page))
        yield p
