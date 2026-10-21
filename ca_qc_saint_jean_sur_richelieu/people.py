import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://sjsr.ca/conseil-municipal/"


class SaintJeanSurRichelieuPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")

        # One card per member: a column holding a photo and a rich-text block
        # like "<strong><a href=profile>Name</a></strong> Conseillère municipale
        # District 1" (or "Maire" for the mayor). Taking the name and district
        # from the cards avoids picking up news articles linked elsewhere.
        cards = page.xpath(
            '//div[contains(@class, "fl-col-content")]'
            '[.//a[contains(@href, "/conseil-municipal/") or contains(@href, "/maire")]][.//img]'
        )
        seen = set()
        count = 0
        for card in cards:
            link = card.xpath('.//p//a[contains(@href, "/conseil-municipal/") or contains(@href, "/maire")]')
            if not link:
                continue
            url = link[0].get("href")
            if url in seen:
                continue
            seen.add(url)

            name = re.sub(r"\s+", " ", link[0].text_content()).strip()
            text = re.sub(r"\s+", " ", card.text_content())
            district_match = re.search(r"District (\d+)", text)

            if "/maire" in url or "Maire" in text:
                role = "Maire"
                district = "Saint-Jean-sur-Richelieu"
            elif district_match:
                role = "Conseiller"
                district = f"District {district_match.group(1)}"
            else:
                continue
            if not name or name == "Vacant":
                continue

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = card.xpath('.//img[contains(@src, "wp-content/uploads")]/@src')
            if image:
                p.image = image[0]

            node = self.lxmlize(url)
            voice = self.get_phone(node, area_codes=[450, 579], error=False)
            if voice:
                p.add_contact("voice", voice, "legislature")

            count += 1
            yield p

        assert count, "No councillors found"
