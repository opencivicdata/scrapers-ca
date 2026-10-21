import re
from collections import defaultdict
from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.norfolkcounty.ca/council-administration-and-government/council/council-members/"


class NorfolkCountyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//section[contains(concat(" ", normalize-space(@class), " "), " usn_cmp_pods ")]'
            '//div[contains(concat(" ", normalize-space(@class), " "), " item ")]'
            '[.//a[contains(@href, "mailto:") and contains(@href, "@norfolkcounty.ca")]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        seat_numbers = defaultdict(int)
        for member in members:
            heading = member.xpath('normalize-space(.//*[contains(@class, "heading")][1])')
            ward_match = re.search(r"Ward\s+(\d+)\s+Councillor", member.text_content())

            if heading.startswith("Mayor "):
                name = heading.replace("Mayor ", "", 1)
                role = "Mayor"
                district = "Norfolk County"
            elif ward_match:
                name = heading
                role = "Councillor"
                ward = f"Ward {ward_match.group(1)}"
                seat_numbers[ward] += 1
                if ward == "Ward 5":
                    district = f"{ward} (seat {seat_numbers[ward]})"
                else:
                    district = ward
            else:
                raise ValueError(f"Unexpected council member block: {heading}")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[226, 289, 365, 519, 548, 905], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
