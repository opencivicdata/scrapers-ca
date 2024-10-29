import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.kawarthalakes.ca/en/municipal-services/contact-a-council-member.aspx"


class KawarthaLakesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath("//tr[.//h2]")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = re.findall(r"(Ward \d)", councillor.text_content())
            if district:
                district = district[0]
                name = re.sub(r"Ward \d|Councillor|Deputy Mayor|-", "", councillor.text_content()).strip()
                role = "Councillor"
            else:
                district = "Kawartha Lakes"
                name = councillor.text_content().replace("Mayor", "").strip()
                role = "Mayor"

            info_node = councillor.xpath("./following-sibling::*")[0]
            email = self.get_email(info_node)
            phone = self.get_phone(info_node)
            image = info_node.xpath("//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            p.image = image
            yield p
