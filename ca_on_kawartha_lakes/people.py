import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.kawarthalakes.ca/government-administration/mayor-and-council/get-to-know-your-council/"


class KawarthaLakesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//div[contains(@class, "item")][.//p[contains(concat(" ", normalize-space(@class), " "), " heading ")]]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            heading = councillor.xpath(
                'normalize-space(.//p[contains(concat(" ", normalize-space(@class), " "), " heading ")])'
            )

            mayor_match = re.match(r"Mayor\s+(.+)", heading)
            councillor_match = re.match(r"(?:Deputy Mayor|Councillor)\s+(.+)", heading)

            if mayor_match:
                district = "Kawartha Lakes"
                name = mayor_match.group(1).strip()
                role = "Mayor"
            elif councillor_match:
                district = councillor.xpath('normalize-space(.//p[contains(@class, "secondary-heading")])')
                name = councillor_match.group(1).strip()
                role = "Councillor"
            else:
                continue

            if "RESIGNED" in name or "Vacant" in name:
                continue

            contact = councillor
            if role == "Mayor":
                contact = councillor.xpath('./following-sibling::div[contains(@class, "item")][1]')
                contact = contact[0] if contact else councillor
            email = self.get_email(contact, error=False)
            phone = self.get_phone(contact, error=False)
            image = councillor.xpath(".//img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            if image:
                p.image = image[0]
            yield p
