import re
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.brandon.ca/city-hall/mayor-and-council/meet-the-mayor-and-councillors/"


class BrandonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(concat(" ", normalize-space(@class), " "), " item_text-below ")]'
            '[.//a[contains(@href, "/meet-the-mayor-and-councillors/") and .//img]]'
        )
        assert len(members) == 11, "Expected 11 council members"

        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            heading = text[0]
            name = text[1]

            if heading == "The Mayor":
                role = "Mayor"
                district = "Brandon"
            else:
                role = "Councillor"
                ward_number = re.search(r"\d+", heading).group(0)
                district = f"Ward {ward_number}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            url = member.xpath('.//a[contains(@href, "/meet-the-mayor-and-councillors/")]/@href')
            if url:
                p.add_source(urljoin(COUNCIL_PAGE, url[0]))

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = re.search(r"[\w.+-]+@brandon\.ca", " ".join(text[2:]))
            if email:
                p.add_contact("email", email.group(0))

            phone = self.get_phone(member, area_codes=[204, 431, 584], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
