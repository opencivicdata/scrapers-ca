from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.longueuil.quebec/fr/conseil-ville"
MAYOR_PAGE = "https://www.longueuil.quebec/fr/conseil/mairesse/biographie"


class LongueuilPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, "utf-8")

        yield self.scrape_mayor(page)

        trs = page.xpath("//tbody/tr")
        assert len(trs), "No councillors found"
        seat_number = 1
        for tr in trs:
            if tr.xpath("./td[2]//text()")[0] != "Vacant":
                district = tr.xpath("./td[1]/text()")[0]
                if "Greenfield Park" in district or "Conseiller n" in district:
                    district = "Greenfield Park (siège {})".format(seat_number)
                    seat_number += 1

                district = {
                    "Fatima-du Parcours-du-Cerf": "Fatima-Parcours-du-Cerf",
                    "LeMoyne-de Jacques-Cartier": "LeMoyne-Jacques-Cartier",
                    "Vieux-Saint-Hubert-de la Savane": "Vieux-Saint-Hubert-la Savane",
                }.get(district, district)

                detail_url = tr.xpath("./td[2]/a/@href")[0]
                detail_page = self.lxmlize(detail_url, "utf-8")

                name = detail_page.xpath("//h1/text()")[0]
                photo_node = detail_page.xpath('//img[contains(@alt, "{0}")]/@src'.format(name))
                if photo_node:
                    photo_url = photo_node[0]
                else:
                    photo_url = detail_page.xpath('//img[contains(@class, "droite")]/@src')[0]

                p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
                p.add_source(COUNCIL_PAGE)
                p.add_source(detail_url)
                p.image = photo_url
                p.add_contact("email", self.get_email(detail_page))
                yield p

    def scrape_mayor(self, page):
        page = self.lxmlize(MAYOR_PAGE)
        img = page.xpath('//img[@class="droite border"]')[0]
        name = img.attrib["alt"]
        p = Person(primary_org="legislature", name=name, district="Longueuil", role="Maire")
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_PAGE)
        p.image = img.attrib["src"]
        p.add_contact("email", self.get_email(page))
        yield p
