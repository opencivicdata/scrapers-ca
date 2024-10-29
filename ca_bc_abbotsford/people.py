from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.abbotsford.ca/council/city-council"
CONTACT_PAGE = "https://www.abbotsford.ca/city-hall/contact-us"


class AbbotsfordPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        coun_page = self.lxmlize(COUNCIL_PAGE)
        contact_page = self.lxmlize(CONTACT_PAGE)
        councillors = coun_page.xpath(
            '//div[@id="block-views-block-council-members-block-1"]//div[@class="views-row"]'
        )
        contact_data = contact_page.xpath('//caption[contains(./h3/text(), "Council")]/following-sibling::tbody//tr')[
            :-1
        ]

        assert len(councillors), "No councillors found"
        assert len(councillors) == len(contact_data), f"Expected {len(councillors)}, got {len(contact_data)}"
        for councillor, contact in zip(councillors, contact_data):
            text = councillor.xpath(".//h3/a")[0].text_content()
            if text.startswith("Councill"):
                role = "Councillor"
                district = f"Abbotsford (seat {councillor_seat_number})"
                councillor_seat_number += 1
            else:
                role = "Mayor"
                district = "Abbotsford"
            name = text.split(" ", 1)[1]
            image = councillor.xpath(".//img/@src")
            email = self.get_email(contact)
            address = contact.xpath("./td[2]//a/text()")[0]
            phone = contact.xpath("./td[2]/div[contains(., 'Phone')]//@href")[0].split(":", 1)[1]
            fax_div = contact.xpath("./td[2]/div[contains(., 'Fax')]//@href")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(CONTACT_PAGE)

            if image:
                p.image = image[0]
            if fax_div:
                fax = fax_div[0].split(":", 1)[1]
                p.add_contact("fax", fax, "legislature")
            p.add_contact("voice", phone, "legislature")
            p.add_contact("address", address, "legislature")
            p.add_contact("email", email)

            yield p
