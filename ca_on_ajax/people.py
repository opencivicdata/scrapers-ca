import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ajax.ca/town-hall/leadership-council/mayor-council/meet-your-mayor-council"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


class AjaxPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=BROWSER_USER_AGENT)

        # One accordion per member, titled either "Mayor Shaun Collier" or
        # "Marilyn Crawford - Regional Councillor Ward 1".
        accordions = page.xpath('//div[contains(@class, "accordion")][.//h3]')
        count = 0
        seen = set()
        for accordion in accordions:
            title = re.sub(r"\s+", " ", accordion.xpath(".//h3")[0].text_content()).strip()
            # Accordion divs can be nested; process each member once.
            if title in seen:
                continue
            seen.add(title)
            mayor_match = re.match(r"^Mayor\s+(.+)$", title)
            councillor_match = re.match(r"^(.+?)\s*[-–]\s*(Regional Councillor|Councillor)\s+(Ward \d+)$", title)
            if mayor_match:
                name, role, district = mayor_match.group(1), "Mayor", "Ajax"
            elif councillor_match:
                name, role, district = councillor_match.groups()
            else:
                continue

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            email = self.get_email(accordion, error=False)
            if email:
                p.add_contact("email", email)
            phone = self.get_phone(accordion, area_codes=[905, 289, 365], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")
            image = [
                src for src in accordion.xpath(".//img/@src") if not re.search(r"logo|icon|ytimg", src, re.IGNORECASE)
            ]
            if image:
                p.image = image[0]

            count += 1
            yield p

        assert count, "No councillors found"
