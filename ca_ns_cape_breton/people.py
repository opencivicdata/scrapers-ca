import re

from utils import CUSTOM_USER_AGENT, CanadianScraper
from utils import CanadianPerson as Person

COUNCIL_PAGE = "https://cbrm.ns.ca/city-hall/councillors/"
MAYOR_PAGE = "https://cbrm.ns.ca/city-hall/mayors-office/"


class CapeBretonPersonScraper(CanadianScraper):
    def get_cape_breton_phone(self, page):
        phone = self.get_phone(page, area_codes=[902], error=False)
        if phone and len(re.sub(r"\D", "", phone)) >= 10:
            return phone
        return None

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=CUSTOM_USER_AGENT)

        councillor_urls = list(
            dict.fromkeys(page.xpath('//a[contains(@href, "/city-hall/councillors/district-")]/@href'))
        )
        assert len(councillor_urls), "No councillor URLs found"

        for url in councillor_urls:
            cpage = self.lxmlize(url, user_agent=CUSTOM_USER_AGENT)

            name = cpage.xpath("//h1/text()")[0].strip()

            district_match = re.search(r"/district-(\d+)/?$", url)
            district = (
                f"District {district_match.group(1)}"
                if district_match
                else cpage.xpath("//h2/text()")[0].strip().split("&")[0].strip()
            )

            phone = self.get_cape_breton_phone(cpage)
            email = self.get_email(cpage, error=False)
            image = cpage.xpath("//img[contains(@alt, 'Councillor')]/@src")

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)
            if image:
                p.image = image[0]

            yield p

        mayorpage = self.lxmlize(MAYOR_PAGE, user_agent=CUSTOM_USER_AGENT)

        # h1 is "Mayor's Office"; the mayor's name is in the first h2
        name = mayorpage.xpath("//h2/text()")[0].strip()
        phone = self.get_cape_breton_phone(mayorpage)
        email = self.get_email(mayorpage, error=False)
        image = mayorpage.xpath('//img[contains(@alt, "Mayor")]/@src')

        p = Person(primary_org="legislature", name=name, district="Cape Breton", role="Mayor")
        p.add_source(MAYOR_PAGE)
        if phone:
            p.add_contact("voice", phone, "legislature")
        if email:
            p.add_contact("email", email)
        if image:
            p.image = image[0]

        yield p
