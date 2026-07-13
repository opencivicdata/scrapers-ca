from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.haltonhills.ca/en/your-government/elected-officials.aspx"

MEMBERS = [
    ("Ann Lawlor", "Mayor", "Halton Hills"),
    ("Clark Somerville", "Regional Councillor", "Wards 1 and 2"),
    ("Jane Fogal", "Regional Councillor", "Wards 3 and 4"),
    ("Alex Hilson", "Councillor", "Ward 1 (seat 1)"),
    ("Michael Albano", "Councillor", "Ward 1 (seat 2)"),
    ("Jason Brass", "Councillor", "Ward 2 (seat 1)"),
    ("Matt Kindbom", "Councillor", "Ward 2 (seat 2)"),
    ("Chantal Garneau", "Councillor", "Ward 3 (seat 1)"),
    ("Ron Norris", "Councillor", "Ward 3 (seat 2)"),
    ("Bob Inglis", "Councillor", "Ward 4 (seat 1)"),
    ("D'Arcy Keene", "Councillor", "Ward 4 (seat 2)"),
]


class HaltonHillsPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        for name, role, district in MEMBERS:
            # Each member's name is an h2 inside a text column that also holds
            # their phone number and (Cloudflare-obfuscated) email address.
            # Member photos are loaded by JavaScript, so no image is scraped.
            blocks = page.xpath(
                '//h2[contains(normalize-space(.), $name)]/ancestor::div[contains(@class, "text_column")][1]',
                name=name,
            )
            assert len(blocks) == 1, f"Expected one profile block for {name}"
            block = blocks[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            email = self.get_email(block, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(block, area_codes=[289, 365, 416, 437, 519, 647, 742, 905], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
