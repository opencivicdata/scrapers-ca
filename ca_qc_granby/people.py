import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.granby.ca/fr/ville/conseil-municipal-de-granby/membres-du-conseil-municipal"


class GranbyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            "//section[.//h2[normalize-space() = 'Cabinet de la mairesse' "
            'or starts-with(normalize-space(), "District ")]]'
        )
        assert len(members) == 11, "Expected 11 council members"

        for member in members:
            heading = member.xpath("normalize-space(.//h2)")
            name = member.xpath("normalize-space(.//p[strong][1]/strong)")

            if heading == "Cabinet de la mairesse":
                role = "Maire"
                district = "Granby"
            else:
                role = "Conseiller"
                district = heading

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath('.//img[contains(@src, "/sites/default/files/")]/@src')
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[450, 579, 438, 514], error=False)
            if phone:
                phone = re.sub(r"\s+", " ", phone)
                p.add_contact("voice", phone, "legislature")

            yield p
