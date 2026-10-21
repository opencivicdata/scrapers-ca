from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.medicinehat.ca/government-city-hall/mayor-city-council-administration/council-members/"


class MedicineHatPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//section[contains(concat(" ", normalize-space(@class), " "), " usn_cmp_pods ")]'
            '//div[contains(concat(" ", normalize-space(@class), " "), " item_text-below ")]'
            '[.//img[contains(@src, "1x1")]]'
        )
        assert len(members) == 9, "Expected 9 council members"

        councillor_seat_number = 1
        for member in members:
            text = [text.strip() for text in member.xpath(".//text()") if text.strip()]
            name = text[0]
            role = text[1]

            if role == "Mayor":
                district = "Medicine Hat"
            else:
                district = f"Medicine Hat (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            image = member.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            phone = self.get_phone(member, area_codes=[368, 403, 587, 780, 825], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
