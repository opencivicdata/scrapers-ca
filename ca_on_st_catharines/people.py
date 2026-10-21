import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

BASE_URL = "https://www.stcatharines.ca"
MAYOR_PAGE = f"{BASE_URL}/council-and-administration/mayor-and-council/mayor-s-office/"
COUNCIL_PAGE = f"{BASE_URL}/council-and-administration/mayor-and-council/ward-councillors/"

WARD_NAMES = {
    "Ward 1": "Merritton",
    "Ward 2": "St. Andrew's",
    "Ward 3": "St. George's",
    "Ward 4": "St. Patrick's",
    "Ward 5": "Grantham",
    "Ward 6": "Port Dalhousie",
}


class StCatharinesPersonScraper(CanadianScraper):
    def scrape(self):
        yield self.scrape_mayor()
        yield from self.scrape_councillors()

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)

        # Name: try h1 first, then look for "Mayor [Name]" in any heading or strong
        name = None
        for el in page.xpath("//h1 | //h2 | //h3 | //strong"):
            text = el.text_content().strip()
            m = re.match(r"Mayor\s+(.+)", text)
            if m and len(m.group(1).split()) >= 2:
                name = m.group(1).strip()
                break
        if not name:
            m = re.search(r"Mayor\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)\s+has served", page.text_content())
            if m:
                name = m.group(1).strip()
        if not name:
            # Fallback: extract from img alt "A headshot of Mayor First Last ..."
            for alt in page.xpath("//img/@alt"):
                m = re.search(r"Mayor\s+([\w][\w\s]+?)(?:\s+with|\s+in|\Z)", alt)
                if m and len(m.group(1).split()) >= 2:
                    name = m.group(1).strip()
                    break
        if not name:
            name = page.xpath("//h1")[0].text_content().strip()

        p = Person(primary_org="legislature", name=name, district="St. Catharines", role="Mayor")
        p.add_source(MAYOR_PAGE)

        phone = page.xpath('//a[starts-with(@href, "tel:")]/@href')
        if phone:
            p.add_contact("voice", p.clean_telephone_number(phone[0].replace("tel:", "")), "legislature")
        email = page.xpath('//a[starts-with(@href, "mailto:")]/@href')
        if email:
            p.add_contact("email", email[0].replace("mailto:", ""))

        img = page.xpath('//img[contains(@alt, "Mayor")]/@src')
        if img:
            src = img[0].split("?")[0]
            p.image = src if src.startswith("http") else BASE_URL + src

        return p

    def scrape_councillors(self):
        page = self.lxmlize(COUNCIL_PAGE)
        cards = page.xpath(
            '//div[contains(@class, "usn_pod")][.//p[contains(@class, "heading")][starts-with(normalize-space(.), "Coun.")]]'
        )
        assert len(cards), "No councillors found"

        seat_numbers = defaultdict(int)

        for card in cards:
            name = card.xpath('normalize-space(.//p[contains(@class, "heading")])').replace("Coun. ", "")
            ward_text = card.xpath(
                'normalize-space(.//div[contains(@class, "text")]//p[starts-with(normalize-space(.), "Ward")][1])'
            )
            if not ward_text and name == "Jackie Lindal":
                ward_text = "Ward 1, Merritton"
            ward_key = ward_text.split(",")[0].strip()
            ward_name = WARD_NAMES.get(ward_key, ward_key)

            seat_numbers[ward_name] += 1
            district = f"{ward_name} (seat {seat_numbers[ward_name]})"

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)

            img = card.xpath(".//img/@src")
            if img:
                src = img[0].split("?")[0]
                p.image = src if src.startswith("http") else BASE_URL + src

            phone = card.xpath('.//a[starts-with(@href, "tel:")]/@href')
            if phone:
                phone_number = phone[0].replace("tel:", "").replace("%20", "").replace(".", "").strip()
                p.add_contact("voice", p.clean_telephone_number(phone_number), "legislature")
            email = card.xpath('.//a[starts-with(@href, "mailto:")]/@href')
            if email:
                p.add_contact("email", email[0].replace("mailto:", ""))

            yield p
