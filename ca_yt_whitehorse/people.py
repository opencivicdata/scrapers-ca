from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.whitehorse.ca/our-government/city-council/mayor-and-council/"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


class WhitehorsePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=BROWSER_USER_AGENT)
        content = page.xpath('//div[contains(@class,"entry-content")]')
        assert content, "entry-content div not found"
        members = content[0].xpath(
            './/p[starts-with(normalize-space(.), "Mayor ") or starts-with(normalize-space(.), "Councillor ")]'
        )
        assert members, "No council member paragraphs found"

        seat = 0
        for para in members:
            first_line = para.text_content().strip().split("\n")[0].strip()

            if first_line.startswith("Mayor "):
                role = "Mayor"
                name = first_line[len("Mayor ") :]
                district = "Whitehorse"
            elif first_line.startswith("Councillor "):
                role = "Councillor"
                name = first_line[len("Councillor ") :]
                seat += 1
                district = f"Whitehorse (seat {seat})"
            else:
                continue

            email = self.get_email(para, error=False)
            phone = self.get_phone(para, area_codes=[867], error=False)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
