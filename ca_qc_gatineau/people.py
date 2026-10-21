import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2fconseil_municipal"
BASE_URL = "http://www.gatineau.ca"


class GatineauPersonScraper(CanadianScraper):
    def name_from_heading(self, text):
        text = text.strip().replace("\xa0", " ")
        for separator in (" \u2013 ", " \u2014 ", " \xe2\u20ac\u201c "):
            if separator in text:
                return text.split(separator, 1)[0].strip()
        return text

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Council members are now listed as plain HTML links in li elements
        councillor_links = page.xpath(
            '//a[contains(@href, "conseil_municipal/district_") or contains(@href, "conseil_municipal/maire")]/@href'
        )
        # Deduplicate while preserving order (page lists each link twice in navigation)
        seen = set()
        unique_links = []
        for link in councillor_links:
            if link not in seen:
                seen.add(link)
                unique_links.append(link)

        councillors = unique_links
        assert councillors, "No councillors found"
        generic_headings = {"En savoir plus", "Dans cette page"}

        for href in councillors:
            profile_url = BASE_URL + href if href.startswith("/") else href
            profile_page = self.lxmlize(profile_url)

            # Determine role and district from URL
            if "/maire" in href:
                role = "Maire"
                district = "Gatineau"
            else:
                role = "Conseiller"
                m = re.search(r"district_(\d+)", href)
                district = "District " + m.group(1) if m else "Gatineau"

            # Photo is a relative image like ../district_1_2.jpg or ../maire_2.jpg
            photo_nodes = profile_page.xpath('//img[contains(@src, "_2.jpg")]/@src')
            photo_url = None
            if photo_nodes:
                src = photo_nodes[0].split("?")[0]  # strip cache-buster
                # The virtual path for p=guichet_municipal/conseil_municipal/district_N
                # means ../file.jpg resolves within /portail/guichet_municipal/conseil_municipal/
                photo_url = urljoin("http://www.gatineau.ca/portail/guichet_municipal/conseil_municipal/", src)

            email = self.get_email(profile_page, error=False)
            phone = self.get_phone(profile_page, error=False)

            # h1 format: "Name – Role text" e.g. "Caroline Murray – Conseillère municipale du district..."
            h1_nodes = profile_page.xpath("//h1")
            name = ""
            if h1_nodes:
                # Take everything before the dash separator.
                name = self.name_from_heading(h1_nodes[0].text_content())
                if name in generic_headings:
                    name = ""
            if not name:
                # Fallback: extract from link text on the main page
                name_link = page.xpath(f'//a[@href="{href}"]')
                if name_link:
                    name = self.name_from_heading(name_link[0].text_content())

            if not name or name == "Vacant" or name in generic_headings:
                continue

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(profile_url)
            if photo_url:
                p.image = photo_url
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
