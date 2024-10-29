import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://nslegislature.ca/members/profiles"


class NovaScotiaPersonScraper(CanadianScraper):
    PARTIES = {
        "Liberal": "Nova Scotia Liberal Party",
        "PC": "Progressive Conservative Association of Nova Scotia",
        "NDP": "Nova Scotia New Democratic Party",
        "Independent": "Independent",
    }

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = page.xpath(
            '//div[contains(@class, "view-display-id-page_mlas_current_tiles")]//div[contains(@class, "views-row-")]'
        )
        assert len(members), "No members found"
        for member in members:
            district = member.xpath('.//div[contains(@class, "views-field-field-constituency")]/div/text()')[0]
            party = member.xpath('.//span[contains(@class, "party-name")]/text()')[0]

            if party == "Vacant":
                continue

            detail_url = member.xpath(".//@href")[0]
            detail = self.lxmlize(detail_url)

            name = detail.xpath('//div[contains(@class, "views-field-field-last-name")]/div/h1/text()')[0]
            name = re.sub(r"(Honourable |\(MLA Elect\)|\(New MLA Elect\))", "", name)
            party = self.PARTIES[party.replace("LIberal", "Liberal")]

            p = Person(primary_org="legislature", name=name, district=district, role="MLA", party=party)
            p.image = detail.xpath('//div[contains(@class, "field-content")]//img[@typeof="foaf:Image"]/@src')[0]

            contact = detail.xpath('//div[contains(@class, "mla-current-profile-contact")]')[0]
            email = self.get_email(contact, error=False)
            if email:
                p.add_contact("email", email)
            p.add_contact("voice", self.get_phone(contact, area_codes=[902]), "constituency")

            p.add_source(COUNCIL_PAGE)
            p.add_source(detail_url)

            address_root = contact.xpath('//h4[contains(text(),"Constituency")]')

            try:
                mailing_address = address_root[0].xpath(
                    '//following-sibling::p[contains(text(),"Mailing address:")]//following-sibling::p[1]/text()'
                )
                civic_address = address = address_root[0].xpath(
                    '//following-sibling::p[contains(text(),"Civic address:")]/text()'
                )
                civic_address_alt = address_root[0].xpath(
                    '//following-sibling::p[contains(text(),"Civic address:")]//following-sibling::p[1]/text()'
                )  # for inconsistent dom
                business_address = address_root[0].xpath(
                    '//following-sibling::h4[contains(text(),"Business address")]//following-sibling::p[2]/text()'
                )
            except Exception:
                pass

            if len(mailing_address) > 0:
                address = mailing_address
            elif len(civic_address) > 0 or len(civic_address_alt) > 0:
                if len(civic_address_alt) > 0:
                    address = civic_address_alt
                else:
                    address = civic_address
                    address.remove(address[0])  # remove civic address
            elif len(business_address) > 0:
                address = business_address

            address = list(map(str.strip, address))
            p.add_contact("address", "\n".join(address), "constituency")

            roles = detail.xpath('//div[contains(@class, "pane-cabinet")]/div//ul/li/div/span/text()')
            linked_roles = detail.xpath('//div[contains(@class, "pane-cabinet")]/div//ul/li/div/span/a/text()')

            if roles or linked_roles:
                roles = [role.strip() for role in roles + linked_roles]
                p.extras["roles"] = roles

            yield p
