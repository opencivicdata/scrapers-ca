import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://repentigny.ca/la-ville/vie-democratique/mairie-elus"


class RepentignyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[contains(@class, "paragraph-counsellors")]//article')
        assert len(members) == 13, "Expected 13 council members"

        for member in members:
            role = member.xpath('normalize-space(.//span[contains(@class, "role")])')
            name = member.xpath("normalize-space(.//h2/a)")
            url = urljoin(COUNCIL_PAGE, member.xpath(".//h2/a/@href")[0])

            if role == "Maire":
                district = "Repentigny"
            else:
                role = "Conseiller"
                detail_page = self.lxmlize(url)
                district = detail_page.xpath(
                    'normalize-space(//*[contains(text(), "District ") and contains(text(), " - ")][1])'
                )
                district = re.sub(r"\s+", " ", district).replace("\u2019", "'")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = member.xpath(".//img/@data-src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[263, 438, 450, 514])
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
