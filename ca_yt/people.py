import contextlib

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://yukonassembly.ca/mlas"


class YukonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//*[@id="block-views-block-members-listing-block-1"]/div/div/div[2]/div')
        assert len(members), "No members found"
        for member in members:
            if "Vacant" not in member.xpath("./div/span")[0].text_content():
                url = member.xpath("./div/span/a/@href")[0]
                page = self.lxmlize(url)
                name = page.xpath("//html/body/div[1]/div/div/section/div[2]/article/div/h1/span/span")[
                    0
                ].text_content()
                district = page.xpath("//div[contains(@class, 'field--name-field-constituency')]/div[2]")[
                    0
                ].text_content()
                party = page.xpath('//div[contains(@class, "field--name-field-party-affiliation")]/div[2]')[0].text

                p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                with contextlib.suppress(IndexError):
                    p.image = page.xpath('//article[contains(@class, "member")]/p/img/@src')[0]

                contact = page.xpath('//article[contains(@class, "members-sidebar")]')[0]
                website = contact.xpath("./div[3]/div[3]/div[2]/a")
                if website:
                    p.add_link(website[0].text_content())

                def handle_address(p, lines, address_type):
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

                def handle_phone(p, lines, phone_type):
                    if "Phone:" in lines:
                        next_line = lines[lines.index("Phone:") + 1]
                        if next_line.endswith(":"):
                            return
                        number = None
                        if "/" in next_line:
                            for fragment in next_line.split("/"):
                                if fragment.strip().startswith("867-"):
                                    number = fragment.strip()
                                    break
                        else:
                            number = next_line
                        p.add_contact("voice", number, phone_type, area_code=867)

                address_lines = contact.xpath("//address//text()")
                contact_lines = contact.xpath("//p[2]//text()")
                assert address_lines[0].strip() == "Yukon Legislative Assembly"
                handle_address(p, address_lines[1:], "legislature")
                handle_phone(p, contact_lines[1:], "legislature")

                email = self.get_email(contact, error=False)
                if email:
                    p.add_contact("email", email)

                yield p
