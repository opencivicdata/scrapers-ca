from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ntassembly.ca/members"


class NorthwestPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath(
            '//*[@id="block-views-members-block-1"]/div/div/table//td[contains(@class, "views-row-members")]'
        )
        assert len(members), "No members found"
        for member in members:
            if "Vacant" not in member.xpath('./div[contains(@class, "views-field-title")]')[0].text_content():
                url = member.xpath("./div/div[1]/a/@href")[0]
                page = self.lxmlize(url)
                name = page.xpath('//*[@id="page-title"]')[0].text_content()
                district = (
                    page.xpath('//*[@id="content"]/div/div[2]/div/div/p[1]')[0]
                    .text_content()
                    .replace("Member ", "")
                    .replace("-", " - ")
                )
                if district == "Mackenzie Delta":
                    district = "Mackenzie-Delta"
                p = Person(primary_org="legislature", name=name, district=district, role="MLA")
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                try:
                    p.image = page.xpath('//article[contains(@class, "member")]/p/img/@src')[0]
                except IndexError:
                    pass

                contact = page.xpath('//*[@id="content"]/div/div[2]/div/div')[0]

                def handle_address(lines, address_type):
                    address_lines = []
                    for line in lines:
                        if line.endswith(":"):  # Room:, Phone:, Fax:
                            break
                        address_lines.append(line)
                    if address_lines:
                        p.add_contact(
                            "address",
                            " ".join(address_lines),
                            address_type,
                        )

                def handle_phone(lines, phone_type):
                    first_phone_added = False
                    for line in lines:
                        if "Phone number:" in line:
                            number = line.replace("Phone number: (867) ", "").replace("Phone number: 867-", "")
                            if first_phone_added:
                                phone_type = "constituency"
                            if number[-4:] == "ext.":
                                number = number.replace("ext.", "")
                            p.add_contact("voice", number, phone_type, area_code=867)
                            first_phone_added = True

                contact_lines = contact.xpath(".//text()")
                handle_address(contact_lines[0:5], "legislature")
                handle_phone(contact_lines[3:], "legislature")

                email = self.get_email(contact, error=False)
                if email:
                    p.add_contact("email", email)
                yield p
