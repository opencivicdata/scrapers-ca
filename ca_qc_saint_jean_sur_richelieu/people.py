from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://sjsr.ca/conseil-municipal/"


class SaintJeanSurRichelieuPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")

        councillors = page.xpath(
            '//div[contains(@class,"fl-module-content fl-node-content")]/div[@class="fl-rich-text"]'
        )[1:]
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//a//text()")[0]
            url = councillor.xpath(".//a//@href")[0]

            if "maire" in url:
                role = "Maire"
                district = "Saint-Jean-sur-Richelieu"
            else:
                role = "Conseiller"
                district = councillor.xpath('.//p[contains(.,"District")]/text()')[-1]

            node = self.lxmlize(url)
            photo_url_rel = node.xpath('//div[@class="fl-photo-content fl-photo-img-jpg"]//img/@src')[0]
            photo_url = urljoin(url, photo_url_rel)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.image = photo_url

            voice = node.xpath(
                '//div[contains(@class,"fl-module-content fl-node-content")]/div[@class="fl-rich-text"]/p[2]/strong//text()'
            )
            if voice:
                p.add_contact("voice", voice[0], "legislature")

            yield p
