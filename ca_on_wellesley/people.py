import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.wellesley.ca/council-and-administration/council/"


def post_number(name):
    return {"Ward One": "Ward 1", "Ward Two": "Ward 2", "Ward Three": "Ward 3", "Ward Four": "Ward 4"}[name]


class WellesleyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # Each member's info is in a paragraph with text like:
        # "Mayor Joe Nowak is serving his third term as Mayor for the Township of Wellesley."
        # "Councillor Shelley Wagner is serving her fifth term as Councillor for Ward One."
        members = page.xpath(
            '//div[contains(@id, "collapse_")]//p[contains(., " is ") and (contains(., "Mayor") or contains(., "Councillor"))]'
        )
        assert members, "No councillors found"

        for member in members:
            text = member.text_content().strip()
            srch = re.search(r"(Mayor|Councillor)\s+(.+?)\s+is\s+.+?\s+for\s+(.+?)\.", text)
            if not srch:
                continue
            position = srch.group(1)
            name = srch.group(2).strip()
            district_raw = srch.group(3).strip()
            phone = self.get_phone(member.getparent())
            email = self.get_email(member.getparent(), error=False)
            district = "Wellesley" if position == "Mayor" else post_number(district_raw)

            p = Person(primary_org="legislature", name=name, district=district, role=position)
            p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            p.add_source(COUNCIL_PAGE)
            yield p
