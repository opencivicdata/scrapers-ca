import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.townofstratford.ca/government/about_our_government/mayor_council"


class StratfordPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE, user_agent="Mozilla/5.0")

        councillors = page.xpath("//tr")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//strong/text()")[0]
            if re.search(r"(?<!Deputy\s)Mayor", name):
                name = name.replace("Mayor ", "")
                role = "Mayor"
                district = "Stratford"
            else:
                name = name.replace("Deputy Mayor ", "").replace("Councillor ", "")
                role = "Councillor"
                area = re.findall(r"(?<=Ward \d,).*", councillor.text_content())[0].strip()
                seat_numbers[area] += 1
                district = f"{area} (seat {seat_numbers[area]})"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath(".//img/@src")[0]

            phone = self.get_phone(councillor)
            email = self.get_email(councillor)

            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)

            yield p
