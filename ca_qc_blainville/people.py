import re
from urllib.parse import urljoin

import lxml.html

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://blainville.ca/ville/portrait-de-blainville/conseil-municipal"


class BlainvillePersonScraper(CanadianScraper):
    def scrape(self):
        response = self.get(COUNCIL_PAGE)
        page = lxml.html.fromstring(response.content.decode("utf-8"))
        members = page.xpath(
            '//ul[contains(concat(" ", normalize-space(@class), " "), " drawers ")]//li[.//h4 and .//h5]'
        )
        assert len(members) == 13, "Expected 13 council members"

        for member in members:
            district_or_title = member.xpath("normalize-space(.//h5)")
            name = member.xpath("normalize-space(.//h4)")

            if district_or_title == "Mairesse de la Ville de Blainville":
                role = "Mairesse"
                district = "Blainville"
            else:
                role = "Conseiller"
                # Post labels use curly apostrophes (e.g. "District d’Alençon (no 8)").
                district = district_or_title.replace("'", "’")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            style = " ".join(member.xpath('.//*[contains(@style, "background-image")]/@style'))
            image = re.search(r"url\(([^)]+)\)", style)
            if image:
                p.image = urljoin(COUNCIL_PAGE, image.group(1))

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            yield p
