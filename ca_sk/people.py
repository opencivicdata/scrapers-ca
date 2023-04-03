from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.legassembly.sk.ca/mlas/"


class SaskatchewanPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//table[@id="MLAs"]//tr')[1:]
        assert len(members), "No members found"
        for member in members:
            if "Vacant" not in member.xpath("./td")[0].text_content():
                name = member.xpath("./td")[0].text_content().split(". ", 1)[1]
                district = member.xpath("./td")[2].text_content()
                url = member.xpath("./td[1]/a/@href")[0]
                page = self.lxmlize(url)
                party = page.xpath(
                    '//span[@id="ContentContainer_MainContent_ContentBottom_Property4"]'
                    '/span'
                )[0].text

                p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                p.image = page.xpath('//div[contains(@class, "mla-image-cell")]/img/@src')[0]

                contact = page.xpath('//div[@id="mla-contact"]/div[2]')[0]
                website = contact.xpath("./div[3]/div[3]/div[2]/a")
                if website:
                    p.add_link(website[0].text_content())

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
                    if "Phone:" in lines:
                        next_line = lines[lines.index("Phone:") + 1]
                        if next_line.endswith(":"):
                            return
                        number = None
                        if "/" in next_line:
                            for fragment in next_line.split("/"):
                                if fragment.strip().startswith("306-"):
                                    number = fragment.strip()
                                    break
                        else:
                            number = next_line
                        p.add_contact("voice", number, phone_type, area_code=306)

                legislature_lines = contact.xpath('.//div[@class="col-md-4"][1]/div//text()')
                assert legislature_lines[0] == "Legislative Building Address"
                handle_address(legislature_lines[1:], "legislature")
                handle_phone(legislature_lines[1:], "legislature")

                constituency_lines = contact.xpath('.//div[@class="col-md-4"][2]/div//text()')
                assert constituency_lines[0] == "Constituency Address"
                handle_address(constituency_lines[1:], "constituency")
                handle_phone(constituency_lines[1:], "constituency")

                email = self.get_email(contact, error=False)
                if email:
                    p.add_contact("email", email)

                yield p
