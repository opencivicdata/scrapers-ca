import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ola.org/en/members/current/contact-information"


class OntarioPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        members = page.xpath('//div[@class="view-content"]//h2')

        headings = {
            "Legislative": "legislature",
            "Ministry": "office",
            "Constituency": "constituency",
        }

        assert len(members), "No members found"
        for member in members:
            name = member.xpath(".//a//text()")[0]
            if "Vacant seat" in name or "Pending " in name:
                continue
            url = member.xpath(".//a//@href")[0]
            node = self.lxmlize(url, encoding="utf-8")
            image = node.xpath('//div[@id="block-views-block-member-member-headshot"]//img/@src')

            district = "".join(node.xpath('//p[@class="riding"]//text()')).strip()
            nodes = node.xpath('//div[@id="main-content"]//a')
            emails = list(filter(None, [self.get_email(node, error=False) for node in nodes]))
            party = node.xpath(
                '//div[contains(@class, "view-display-id-current_party_block")]//div[@class="view-content"]//text()'
            )

            party = next((item.strip() for item in party if item.strip()), "Independent")
            p = Person(primary_org="legislature", name=name, district=district, role="MPP", party=party)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            if image:
                p.image = image[0]

            if emails:
                p.add_contact("email", emails.pop(0))
                if emails:
                    p.extras["constituency_email"] = emails.pop(0)

            for heading, note in headings.items():
                office = node.xpath(f'//h3[contains(., "{heading}")]')
                if office:
                    try:
                        office_info = office[0].xpath(
                            '../following-sibling::div[@class="views-field views-field-nothing"]//span[@class="field-content"]//text()'
                        )
                        office_items = [item for item in office_info if item.strip()]
                        office_items = list(map(str.strip, office_items))

                        phone_index = office_items.index("Tel.:")
                        phone = office_items[phone_index + 1]

                        fax = None
                        if "Fax:" in office_items:
                            fax_index = office_items.index("Fax:")
                            if fax_index + 1 < len(office_items):
                                fax = office_items[fax_index + 1]

                        regex = re.compile(
                            r"(\b[\w.-]+@+[\w.]+.+[\w.]\b)|(\d{3}[-\.\s]\d{3}[-\.\s]\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]\d{4}|\d{3}[-\.\s]\d{4})|(?:Tel.:)|(?:Fax:)|(?:Toll free:)"
                        )  # remove none address items
                        address = [i for i in office_items if not regex.match(i)]
                    except Exception:
                        pass
                    else:
                        if phone:
                            p.add_contact("voice", phone, note)
                        if fax:
                            p.add_contact("fax", fax, note)
                        if address:
                            p.add_contact("address", "\n".join(address), note)

            roles = node.xpath(
                '//div[contains(@class, "view-display-id-member_current_role_block")]'
                '//ul/li/span[@aria-hidden="true"]/text()'
            )

            if roles:
                roles = [role.strip() for role in roles if role.strip()]
                p.extras["roles"] = roles

            yield p
