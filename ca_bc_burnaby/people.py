from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.burnaby.ca/our-city/mayor-and-council"


class BurnabyPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath("//a[@class='biography__link']/@href")
        assert len(councillors), "No councillors found"
        for person_url in councillors:
            page = self.lxmlize(person_url)

            role, name = page.xpath("//h1/span")[0].text_content().strip().split(" ", 1)
            photo_url = page.xpath('//img[@typeof="foaf:Image"]/@src')[0]

            contact_node = page.xpath('//div[@class="contact"]')[0]

            email = self.get_email(contact_node)
            phone = self.get_phone(contact_node, area_codes=[604, 778])

            if role == "Mayor":
                district = "Burnaby"
            else:
                district = f"Burnaby (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
