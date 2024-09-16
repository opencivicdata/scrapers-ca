from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.tol.ca/en/the-township/councillors.aspx"
MAYOR_PAGE = "https://www.tol.ca/en/the-township/mayor.aspx"


class LangleyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        seat_number = 1
        councillors = page.xpath('//a[contains(@target,"_self")]/@href')
        assert len(councillors), "No councillors found"
        for url in councillors:
            page = self.lxmlize(url)
            name = page.xpath("//h1")[0].text_content().strip()

            district = f"Langley (seat {seat_number})"
            seat_number += 1
            email = self.get_email(page)
            phone = self.get_phone(page)

            p = Person(primary_org="legislature", name=name, role="Councillor", district=district)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            yield p
        page = self.lxmlize(MAYOR_PAGE)
        name = page.xpath("//h1")[0].text_content().replace("Mayor", "").strip()
        email = self.get_email(page)
        phone = self.get_phone(page)
        address_block = page.xpath('//p/a[@rel="noopener noreferrer"]/parent::p')[0].text_content()
        line1 = address_block[address_block.find("Facility") + 8 : address_block.find("Langley,")]
        line2 = address_block[address_block.find("Langley,") : address_block.find("Phone") - 1]
        address = f"{line1}, {line2}"
        p = Person(primary_org="legislature", name=name, role="Mayor", district="Langley")
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("address", address, "legislature")
        p.add_source(MAYOR_PAGE)
        yield p
