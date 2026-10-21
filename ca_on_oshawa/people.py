import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.oshawa.ca/city-hall/city-council/council-members/"


class OshawaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        # One card per member: div.inner with a p.heading (name), a role
        # paragraph like "Ward 1 Regional & City Councillor", and contacts.
        cards = [
            card
            for card in page.xpath(
                '//div[contains(@class, "inner")][.//p[contains(@class, "heading")]][.//a[contains(@href, "mailto:")]]'
            )
            # Containers nest; a member card holds exactly one heading.
            if len(card.xpath('.//p[contains(@class, "heading")]')) == 1
        ]
        assert cards, "No council member headings found"

        for card in cards:
            name = card.xpath('.//p[contains(@class, "heading")]')[0].text_content().strip()
            text = re.sub(r"\s+", " ", card.text_content())

            if re.search(r"\bMayor\b", text) and "Ward" not in text:
                role, district = "Mayor", "Oshawa"
            else:
                ward_match = re.search(r"(Ward \d+) (Regional & City Councillor|City Councillor)", text)
                if not ward_match:
                    continue
                district = ward_match.group(1)
                role = "Regional Councillor" if "Regional" in ward_match.group(2) else "Councillor"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            email = self.get_email(card, error=False)
            if email:
                p.add_contact("email", email)
            phone = self.get_phone(card, error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")
            image = card.xpath(".//img/@src")
            if image:
                p.image = image[0]

            yield p
