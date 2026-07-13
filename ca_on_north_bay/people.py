from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://northbay.ca/city-government/mayor-council/contact-info-appointments-bios/"


class NorthBayPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        cards = page.xpath('//div[contains(concat(" ", normalize-space(@class), " "), " card ")][.//h5]')
        assert len(cards) == 11, "Expected 11 council members"

        councillor_seat_number = 1
        for card in cards:
            name = card.xpath("normalize-space(.//h5)")
            role_text = card.xpath("normalize-space(.//p[1])")
            if role_text == "Mayor":
                role = "Mayor"
                district = "North Bay"
            else:
                role = "Councillor"
                district = f"North Bay (seat {councillor_seat_number})"
                councillor_seat_number += 1

            detail_url = urljoin(
                COUNCIL_PAGE,
                card.xpath('.//a[contains(@href, "contact-info-appointments-bios")]/@href')[0],
            )
            detail_page = self.lxmlize(detail_url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            image = card.xpath(".//img/@src")
            if image:
                p.image = urljoin(COUNCIL_PAGE, image[0])

            email = self.get_email(detail_page, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(detail_page, area_codes=[249, 683, 705], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
