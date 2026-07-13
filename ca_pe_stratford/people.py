import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://townofstratford.ca/government-services/contact-town-of-stratford/mayor-council/"


class StratfordPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.cloudscrape(COUNCIL_PAGE)

        # One paragraph per member, e.g. "<strong>Councillor Jill Chandler</strong>,
        # Ward 2, Stewart Cove ... E: <obfuscated email> P: 902-940-6981".
        members = page.xpath('//p[.//strong][contains(., "P:")]')
        count = 0
        for member in members:
            name = re.sub(r"\s+", " ", member.xpath(".//strong")[0].text_content()).strip()
            if not re.match(r"(Deputy )?Mayor |Councillor ", name):
                continue
            text = re.sub(r"\s+", " ", member.text_content()).replace("’", "'")

            if re.match(r"Mayor ", name):
                name = name.replace("Mayor ", "")
                role = "Mayor"
                district = "Stratford"
            else:
                name = name.replace("Deputy Mayor ", "").replace("Councillor ", "")
                role = "Councillor"
                area = re.search(r"Ward \d+,\s*([A-Za-z' ]+?)\s*(?:Chair|Vice|E:|P:|$)", text).group(1)
                seat_numbers[area] += 1
                district = f"{area} (seat {seat_numbers[area]})"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            phone = self.get_phone(member, area_codes=[902])
            email = self.get_email(member, error=False)

            p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)

            count += 1
            yield p

        assert count, "No councillors found"
