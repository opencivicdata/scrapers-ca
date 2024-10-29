from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://city.langley.bc.ca/cityhall/city-council/council-members"


class LangleyPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//div[@class="field field--name-field-ec-section-title field--type-string field--label-hidden field__item"]'
        )[:-1]

        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, name = councillor.text_content().split(" ", 1)
            if role == "Mayor":
                district = "Langley"
                phone_div = councillor.xpath('..//p[contains(., "Phone:")]')[0]
                phone = self.get_phone(phone_div)
            else:
                district = f"Langley (seat {councillor_seat_number})"
                phone = (
                    "604 514 2800"  # According to their site, all councillors can be contacted at this phone number
                )
                councillor_seat_number += 1
            email = (
                councillor.xpath('..//p[contains(., "Email:")]')[0]
                .text_content()
                .split("Email:", 1)[1]
                .strip()
                .replace("(at)", "@")
            )
            image = councillor.xpath("..//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            p.add_source(COUNCIL_PAGE)

            yield p
