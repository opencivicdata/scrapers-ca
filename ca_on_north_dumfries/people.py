import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.northdumfries.ca/en/township-services/mayor-and-council.aspx"


class NorthDumfriesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        word_to_number = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
        }

        councillors = page.xpath("//table[2]//tr[position() mod 2 = 1]")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            match = re.match(r"(?:Ward (\S+) )?(Mayor|Councillor) (.+)", councillor.text_content().strip())
            role = match.group(2)
            name = match.group(3)

            district = "North Dumfries" if role == "Mayor" else f"Ward {word_to_number[match.group(1)]}"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            node = councillor.xpath("./following-sibling::tr/td")[0]
            p.add_contact("voice", self.get_phone(node), "legislature")

            value = node.xpath(".//a/@href")[0]
            if not value.startswith("javascript:"):
                p.add_contact("email", value.replace("mailto:", ""))

            yield p
