from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.portcoquitlam.ca/our-government/city-council"


class PortCoquitlamPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//h3[contains(@class, "field-content")]/ancestor::*[contains(@class, "views-row")][1]')
        assert len(members) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for member in members:
            title = member.xpath("normalize-space(.//h3)")
            url = urljoin(COUNCIL_PAGE, member.xpath(".//h3/a/@href")[0])
            detail_page = self.lxmlize(url)

            if title.startswith("Mayor "):
                role = "Mayor"
                name = title.replace("Mayor ", "", 1)
                district = "Port Coquitlam"
            else:
                role = "Councillor"
                name = title.replace("Councillor ", "", 1)
                district = f"Port Coquitlam (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = detail_page.xpath('//main//img[contains(@src, "/sites/default/files/")]/@src')
            if image:
                p.image = urljoin(url, image[0])

            email = self.get_email(member, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(member, area_codes=[236, 604, 672, 778], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
