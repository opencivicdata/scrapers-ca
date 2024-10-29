import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.wellesley.ca/council/councillors/?q=council/councillors"


def post_number(name):
    return {"Ward One": "Ward 1", "Ward Two": "Ward 2", "Ward Three": "Ward 3", "Ward Four": "Ward 4"}[name]


class WellesleyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        members = [
            el
            for el in page.xpath('//div//td[@data-name="accChild"]')
            if el.text_content().strip().lower().split()[0] in ["mayor", "councillor"]
        ]
        assert len(members), "No councillors found"

        for member in members:
            position = member.text_content().split()[0]
            srch = re.search(r"\w+(.+?) is.*? for (.+?)\.", member.text_content().strip())
            name = srch.group(1).strip()
            district = srch.group(2).strip()
            phone = self.get_phone(member)
            email = self.get_email(member, error=False)
            district = "Wellesley" if position == "Mayor" else post_number(district)

            p = Person(primary_org="legislature", name=name, district=district, role=position)
            p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            p.add_source(COUNCIL_PAGE)
            yield p
