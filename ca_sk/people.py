import contextlib
import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.legassembly.sk.ca/mlas/"


class SaskatchewanPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        members = page.xpath('//table[@id="mla-table"]//tr')[1:]
        assert len(members), "No members found"
        for member in members:
            if "Vacant" in member.xpath("./td")[1].text_content():
                continue
            name = member.xpath("./td")[0].text_content().split(". ", 1)[1].strip()
            district = member.xpath("./td")[2].text_content().strip()
            url = member.xpath("./td[1]/a/@href")[0]
            page = self.lxmlize(url)
            party = page.xpath('//div[contains(@class, "mla-header")]')[0].text.split(" - ")[1].strip()

            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            with contextlib.suppress(IndexError):
                p.image = page.xpath('//div[contains(@class, "mla-image-cell")]/img/@src')[0]

            def handle_address(p, lines, address_type):
                address_lines = []
                for line in lines:
                    if re.match(r"(Room|Phone|Fax)\:", line):
                        break
                    address_lines.append(line)
                if address_lines:
                    p.add_contact(
                        "address",
                        " ".join(address_lines),
                        address_type,
                    )

            def handle_phone(p, lines, phone_type):
                matches = re.findall(r"Phone\:\s*(306-[\d\-]+)", "\n".join(lines))
                if len(matches) == 1:
                    p.add_contact("voice", matches[0], phone_type, area_code=306)

            for address in page.xpath('//div[@class="col-md-3"]'):
                lines = address.xpath("./div//text()")
                address_type = None
                if lines[0] == "Legislative Building Address":
                    address_type = "legislature"
                elif lines[0] == "Constituency Address":
                    address_type = "constituency"
                else:
                    raise AssertionError(f"Unexpected address type: {lines[0]}")
                handle_address(p, lines[1:], address_type)
                handle_phone(p, lines[1:], address_type)

            email = self.get_email(page.xpath('//div[@id="content"]')[0], error=False)
            if email:
                p.add_contact("email", email)

            websites = re.findall(
                r"Website:\s*(http\S+)", " ".join(page.xpath('//div[@class="col-md-4"]/div//text()'))
            )
            if len(websites) == 1:
                p.add_link(websites[0])

            yield p
