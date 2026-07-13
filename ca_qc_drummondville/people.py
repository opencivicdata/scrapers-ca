import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.drummondville.ca"
COUNCIL_PAGE = f"{BASE_URL}/mairie-et-vie-municipale/conseil-municipal/profil-des-conseillers/"
MAYOR_PAGE = f"{BASE_URL}/author/jfhoule_mairie/"


class DrummondvillePersonScraper(CanadianScraper):
    def scrape(self):
        mayor_page = self.lxmlize(MAYOR_PAGE)
        name = mayor_page.xpath("normalize-space(//h1)")
        name = re.sub(r"^(?:M\.|Mme)\s+", "", name).replace(", maire", "")

        p = Person(primary_org="legislature", name=name, district="Drummondville", role="Maire")
        p.add_source(MAYOR_PAGE)

        image = mayor_page.xpath('//img[contains(@src, "_Profil_")]/@src')
        if image:
            p.image = urljoin(MAYOR_PAGE, image[0])

        yield p

        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " liste-conseiller ")]')
        assert len(members) == 12, "Expected 12 councillors"

        for member in members:
            district = member.xpath('normalize-space(.//div[contains(@class, "billet-top")])')
            name = member.xpath('normalize-space(.//p[contains(@class, "titre-conseiller")])')
            name = re.sub(r"^(?:M\.|Mme)\s+", "", name)
            url = urljoin(COUNCIL_PAGE, member.xpath(".//a/@href")[0])

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            yield p
