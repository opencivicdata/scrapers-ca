import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

LISTING_URL = "https://ville.vaudreuil-dorion.qc.ca/fr/la-ville/conseil-municipal/maire-et-conseillers-municipaux"


class VaudreuilDorionPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(LISTING_URL)
        # Cards are <a> wrapping an h3 name; hrefs are absolute URLs under
        # /fr/la-ville/mairie/conseil-municipal/.
        cards = page.xpath('//a[.//h3 and contains(@href, "/fr/la-ville/mairie/conseil-municipal/")]')
        assert cards, "No member cards found"
        for card in cards:
            name = re.sub(r"\s+", " ", card.xpath(".//h3")[0].text_content()).strip()
            if not name:
                continue
            profile_url = card.get("href")

            if "c-team_mayor" in (card.get("class") or ""):
                role, district = "Mayor", "Vaudreuil-Dorion"
            else:
                district_p = card.xpath('.//p[contains(@class, "district")]/text()')
                match = re.search(r"District (\d+)", district_p[0]) if district_p else None
                if not match:
                    continue
                role, district = "Councillor", f"District {match.group(1)}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(LISTING_URL)
            p.add_source(profile_url)

            image = card.xpath('.//div[contains(@style, "background-image")]/@style')
            if image:
                match = re.search(r"url\('([^']+)'\)", image[0])
                if match:
                    p.image = match.group(1)

            ppage = self.lxmlize(profile_url)
            main = ppage.xpath("//main")
            email = self.get_email(main[0] if main else ppage, error=False)
            if email:
                p.add_contact("email", email)

            yield p
