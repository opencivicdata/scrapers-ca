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
            def decode_email(e):
                de = ""
                k = int(e[:2], 16)

                for i in range(2, len(e)-1, 2):
                    de += chr(int(e[i:i+2], 16)^k)

                return de
            page = self.lxmlize(person_url)

            role, name = page.xpath("//h1/span")[0].text_content().strip().split(" ", 1)
            photo_url = page.xpath('//img[@typeof="foaf:Image"]/@src')[0]

            contact_node = page.xpath('//div[@class="contact"]')[0]

            email = page.xpath('//div[@class = "contact__detail contact__detail--email"]/a/@href')[0]
            decoded_email = decode_email(email.split("#",1)[1]) # cloudflare encrypts the email data when accessed by a bot

            phone = self.get_phone(contact_node, area_codes=[604, 778])

            if role == "Mayor":
                district = "Burnaby"
            else:
                district = "Burnaby (seat {})".format(councillor_seat_number)
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_source(person_url)
            if email:
                p.add_contact("email", decoded_email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
