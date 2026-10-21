import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.conceptionbaysouth.ca/council/councillors/"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)

MEMBERS = [
    ("Darrin Bent", "Mayor", "Conception Bay South"),
    ("Andrea Gosse", "Councillor", "Ward 2"),
    ("Shelley Moores", "Councillor", "Ward 1"),
    ("Gerard Tilley", "Councillor", "Ward 3"),
    ("Melissa Hardy", "Councillor", "Ward 4"),
    ("Joshua Barrett", "Councillor at Large", "Conception Bay South (seat 1)"),
    ("Christine Butler", "Councillor at Large", "Conception Bay South (seat 2)"),
    ("Rex Hillier", "Councillor at Large", "Conception Bay South (seat 3)"),
    ("Warrick Cluney", "Councillor at Large", "Conception Bay South (seat 4)"),
]


class ConceptionBaySouthPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=BROWSER_USER_AGENT, verify=False)
        text = page.text_content()
        for name, role, district in MEMBERS:
            m = re.search(rf"{re.escape(name)}.*?(\(?709\)?[-\s.]\d{{3}}[-\s.]\d{{4}})", text, re.S)
            phone = m.group(1) if m else None
            image = page.xpath(
                f'//img[not(starts-with(@src, "data:")) and (contains(@alt, "{name}") or contains(@data-src, "{name.split()[0]}") or contains(@src, "{name.split()[0]}"))]/@src'
            )
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
