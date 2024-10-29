import contextlib

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.assembly.nu.ca/members/mla"


class NunavutPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//*[@id="content"]/section/div/div[3]/div/div[2]/div')
        assert len(members), "No members found"
        for member in members:
            if "Vacant" in member.xpath("./span[2]")[0].text_content():
                continue
            url = member.xpath("./span[1]/span/a/@href")[0]
            page = self.lxmlize(url)
            name = page.xpath("//span[contains(@class, 'field--name-title')]")[0].text_content()
            district = page.xpath("//div[contains(@class, 'field--name-field-member-mla')]/div[2]")[0].text_content()
            party = ""
            name = name.replace("The Honourable ", "").replace("The honourable ", "")
            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            with contextlib.suppress(IndexError):
                p.image = page.xpath('//div[contains(@class, "field--name-field-member-photo")]/div[2]/img/@src')[0]

            contact = page.xpath('//div[contains(@class, "field--name-field-member-constituency")]/div[2]/div/p')[0]
            website = contact.xpath("./div[3]/div[3]/div[2]/a")
            if website:
                p.add_link(website[0].text_content())

            def handle_address(p, lines, address_type):
                address_lines = []
                for line in lines:
                    if ":" in line.strip():  # Room:, Phone:, Fax:
                        break
                    address_lines.append(line.strip())
                if address_lines:
                    p.add_contact(
                        "address",
                        " ".join(address_lines),
                        address_type,
                    )

            def handle_phone(p, lines, phone_type):
                for line in lines:
                    if "Phone:" in line:
                        number = line.replace("Phone: (867) ", "")
                        p.add_contact("voice", number, phone_type, area_code=867)

            address_lines = contact.xpath("./text()")
            handle_address(p, address_lines, "legislature")
            handle_phone(p, address_lines, "legislature")

            email = self.get_email(contact, error=False)
            if email:
                p.add_contact("email", email)

            yield p
