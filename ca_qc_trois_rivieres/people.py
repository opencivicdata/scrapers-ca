import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = (
    "https://www.v3r.net/a-propos-de-la-ville/vie-democratique/conseil-municipal/maire-et-conseillers-municipaux"
)


class TroisRivieresPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Each councillor has a "Voir la fiche" link to their profile page
        profile_links = page.xpath('//a[contains(normalize-space(.), "Voir la fiche")]/@href')
        assert len(profile_links), "No councillors found"

        for href in profile_links:
            url = urljoin(COUNCIL_PAGE, href)
            profile_page = self.lxmlize(url)

            email = self.get_email(profile_page, error=False)

            # Name is in h3 heading
            name_nodes = profile_page.xpath("//h3")
            name = name_nodes[0].text_content().strip() if name_nodes else ""

            # District from h2 heading (e.g. "District du Carmel") or "Maire de Trois-Rivières"
            district_nodes = profile_page.xpath(
                '//h2[contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "district")'
                ' or contains(translate(., "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz"), "maire")]'
            )
            raw_district = district_nodes[0].text_content().strip() if district_nodes else ""

            if "maire" in url.lower() or "Maire" in raw_district:
                district = "Trois-Rivières"
                role = "Maire"
            else:
                # "District du Carmel" → "du Carmel" (strip "District " prefix, lowercase preposition)
                district = re.sub(r"\ADistrict\s+", "", raw_district, flags=re.IGNORECASE).strip()
                district = re.sub(
                    r"\A(de|des|du)\s+",
                    lambda m: m.group(1).lower() + " ",
                    district,
                    flags=re.IGNORECASE,
                )
                if not district:
                    district = raw_district
                role = "Conseiller"

            # Photo from WordPress uploads
            photo_nodes = profile_page.xpath('//img[contains(@src, "wp-content/uploads")]/@src')
            photo_url = photo_nodes[0] if photo_nodes else None

            if not name:
                continue

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            if photo_url:
                p.image = photo_url
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            if email:
                p.add_contact("email", email)
            yield p
