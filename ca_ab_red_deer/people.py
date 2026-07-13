from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.reddeer.ca"
COUNCIL_PAGE = f"{BASE_URL}/city-government/mayor-and-city-councillors/city-council/city-council-profiles/"


class RedDeerPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        profiles = page.xpath('//section[contains(@class, "content")]//h3/a[@href]')

        assert len(profiles) == 9, "Expected 9 council profiles"

        councillor_seat_number = 1
        for profile in profiles:
            title = profile.text_content().strip()
            role, name = title.split(" ", 1)
            url = urljoin(BASE_URL, profile.get("href"))

            if role == "Mayor":
                district = "Red Deer"
            else:
                district = f"Red Deer (seat {councillor_seat_number})"
                councillor_seat_number += 1

            profile_page = self.lxmlize(url)
            content = profile_page.xpath('//section[contains(@class, "content")]')[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = content.xpath(".//img/@src")
            if image:
                p.image = urljoin(BASE_URL, image[0])

            email = self.get_email(content, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(content, area_codes=[403, 587, 825, 368], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
