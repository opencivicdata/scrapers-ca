import contextlib

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ntlegislativeassembly.ca/members/members-legislative-assembly/members"


class NorthwestTerritoriesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//div[contains(@class, "view-id-member")]/div/div[contains(@class, "views-row")]')
        assert len(members), "No members found"
        for member in members:
            if "Vacant" not in member.xpath('//span[contains(@class, "field--name-title")]')[0].text_content():
                url = member.xpath("./article/a/@href")[0]
                page = self.lxmlize(url)
                name = page.xpath('//*[contains(@class, "page-title")]')[0].text_content().strip()
                district = (
                    page.xpath('//*[contains(@class, "field--name-field-constituency")]')[0]
                    .text_content()
                    .replace("Member ", "")
                    .replace(" - ", "-")
                )
                p = Person(primary_org="legislature", name=name, district=district, role="MLA")
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                with contextlib.suppress(IndexError):
                    p.image = page.xpath('//div[contains(@class, "field--name-field-media-image")]/img/@src')[0]

                contact = page.xpath('//*[contains(@class, "paragraph--type--office")]')[0]
                if len(contact.xpath('./div[contains(@class, "office-address-wrapper")]')) == 0:
                    address_section = page.xpath('//*[contains(@class, "paragraph--type--office")]')[1]
                else:
                    address_section = contact

                def handle_address(p, contact, address_type):
                    address_lines = []
                    po_box_line = (
                        "PO Box "
                        + contact.xpath('./div[contains(@class, "office-address-wrapper")]/div[2]/div[2]')[0]
                        .text_content()
                        .strip()
                    )
                    address_lines.append(po_box_line)
                    address_lines.append(
                        contact.xpath('./div[contains(@class, "office-address-wrapper")]/div[1]/p')[0]
                        .text_content()
                        .strip()
                    )
                    if address_lines:
                        p.add_contact(
                            "address",
                            " ".join(address_lines),
                            address_type,
                        )

                def handle_phone(p, lines, phone_type):
                    first_phone_added = False
                    for line in lines:
                        if "Assistant" in line.strip():
                            return
                        if "867" in line.strip():
                            number = line.strip().replace("(867) ", "").replace("867-", "")
                            if first_phone_added:
                                phone_type = "constituency"
                            if number[-4:] == "ext.":
                                number = number.replace("ext.", "")
                            p.add_contact("voice", number, phone_type, area_code=867)
                            first_phone_added = True

                contact_lines = contact.xpath(".//text()")
                handle_address(p, address_section, "legislature")
                handle_phone(p, contact_lines, "legislature")

                email_elements = page.xpath(
                    '//*[contains(@class, "field--paragraph--field-email")]/div[@class="field__item"]'
                )
                for element in email_elements:
                    email = self.get_email(element, error=False)
                    if email:
                        p.add_contact("email", email)

                yield p
