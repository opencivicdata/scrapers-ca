import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.assembly.pe.ca/members"


class PrinceEdwardIslandPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath('//div[@class="views-row"]')

        assert len(members), "No members found"
        for member in members:
            if not member.text_content().strip():
                continue

            title = member.xpath('.//span[contains(@class, "member-title")]//a[1]')[0]
            district = member.xpath('.//div[contains(@class, "views-field-field-member-constituency")]//text()')[0]
            party = member.xpath('.//div[contains(@class, "views-field-field-member-pol-affiliation")]//text()')[0]
            url = title.attrib["href"]
            p = Person(
                primary_org="legislature",
                name=title.text.split(",")[0],
                district=district,
                party={
                    "Green": "Green Party of Prince Edward Island",
                    "PC": "Progressive Conservative Party of Prince Edward Island",
                    "Liberal": "Liberal Party of Prince Edward Island",
                }.get(party, party),
                role="MLA",
            )
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            details = self.lxmlize(url)
            p.image = details.xpath('//div[contains(@class, "member-portrait")]//img')[0].get("src")
            info = details.xpath('//div[contains(@class, "member-contact-info")]')[0]

            phone = re.search(r"(?:Telephone|Tel|Phone):\s*(.+?)\n", info.text_content())
            if phone:
                p.add_contact("voice", phone.group(1), "legislature")
            address = re.search(
                r"(?:Office location):\s*(.+)\n*(.+)\n(175 Richmond Street|175 Richmond Street.+)\n(.+)",
                info.text_content(),
            )  # Richmond Street is the legislature
            if address:
                address = address.group(1) + " " + address.group(2) + " " + address.group(3) + " " + address.group(4)
                p.add_contact("address", address, "legislature")

            email = self.get_email(info, error=False)
            if email:
                p.add_contact("email", email)

            roles = details.xpath(
                '//td[contains(@class, "end-date") and contains(text(), "Current")]/preceding-sibling::td[contains(@class, "role-name")]/text()'
            )
            if roles:
                p.extras["roles"] = [role.strip() for role in roles]

            yield p
