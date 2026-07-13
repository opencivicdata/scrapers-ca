from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://stalbert.ca/cosa/leadership/council/profiles/"


class StAlbertPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        urls = []
        for href in page.xpath('//article//a[contains(@href, "/cosa/leadership/council/profiles/")][.//img]/@href'):
            url = urljoin(COUNCIL_PAGE, href)
            if url not in urls:
                urls.append(url)
        assert len(urls) == 7, "Expected 7 council profiles"

        councillor_seat_number = 1
        for url in urls:
            profile_page = self.lxmlize(url)
            title = profile_page.xpath("normalize-space(//article//h1[1])")
            if title == "Emergency Notice":
                title = profile_page.xpath("normalize-space(//article//*[self::h2 or self::h3][1])")

            if title.startswith("Mayor "):
                role = "Mayor"
                name = title.replace("Mayor ", "", 1)
                district = "St. Albert"
            else:
                role = "Councillor"
                name = title.replace("Councillor ", "", 1)
                district = f"St. Albert (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = profile_page.xpath('//article//img[contains(@src, "/site/assets/files/")]/@src')
            if image:
                p.image = urljoin(url, image[0])

            contact = profile_page.xpath('//aside[contains(translate(., "contact", "CONTACT"), "CONTACT")][last()]')
            if contact:
                email = self.get_email(contact[0], error=False)
                if email:
                    p.add_contact("email", email)

                phone = self.get_phone(contact[0], area_codes=[368, 403, 587, 780, 825], error=False)
                if phone:
                    p.add_contact("voice", phone, "legislature")

            yield p
