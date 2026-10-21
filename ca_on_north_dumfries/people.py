import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.northdumfries.ca/township-services/mayor-and-council/"


class NorthDumfriesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        word_to_number = {
            "One": 1,
            "Two": 2,
            "Three": 3,
            "Four": 4,
        }

        # Collapsible sections; the trigger link text is "Mayor Sue Foxton"
        # or "Ward One Councillor Rod Rolleman"
        councillors = page.xpath('//a[contains(@href, "#collapse_")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            heading = councillor.text_content().strip()
            match = re.match(r"(?:Ward (\S+) )?(Mayor|Councillor) (.+)", heading)
            if not match:
                continue
            role = match.group(2)
            name = match.group(3).strip()
            district = "North Dumfries" if role == "Mayor" else f"Ward {word_to_number[match.group(1)]}"

            # The content panel follows the trigger; find the collapse div by href target
            collapse_id = councillor.get("href").rsplit("#", 1)[-1]
            panel = page.xpath(f'//div[@id="{collapse_id}"]')
            if not panel:
                continue
            panel = panel[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", self.get_phone(panel), "legislature")
            p.add_contact("email", self.get_email(panel))

            yield p
