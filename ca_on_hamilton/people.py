import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.hamilton.ca/city-council/council-committee/city-council-members/city-councillors"
MAYOR_PAGE = "https://www.hamilton.ca/city-council/council-committee/city-council-members/mayor-andrea-horwath"
BROWSER_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36"
)


class HamiltonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, user_agent=BROWSER_USER_AGENT)

        yield self.mayor_data(MAYOR_PAGE)

        councillors = page.xpath('//div[contains(@class, "image-cta-card")]//@href[1]')
        assert len(councillors), "No councillors found"
        for url in councillors:
            yield self.councillor_data(url)

    def councillor_data(self, url):
        page = self.lxmlize(url, user_agent=BROWSER_USER_AGENT)

        district = page.xpath("//h1/text()")[0]
        name = page.xpath('//h2[@class="title"]/text()')[0].split("(")[0].strip()
        info_node = page.xpath(
            '//div[@class="section container-md image--right post-card post-card--large bg--#FFFFFF"]'
        )[0]
        phone = self.get_phone(info_node, area_codes=[289, 365, 905], error=False)
        email = self.get_email(info_node)
        photo_url = info_node.xpath(".//img/@src")  # can be empty

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact("email", email)

        if phone:
            p.add_contact("voice", phone, "legislature")
        if photo_url:
            p.image = photo_url[0]

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url, user_agent=BROWSER_USER_AGENT)
        # The h1 is "Mayor Andrea Horwath"; contact is a phone number in the
        # page body (email is behind a contact form).
        name = re.sub(r"^Mayor\s+", "", page.xpath("//h1/text()")[0].strip())

        p = Person(primary_org="legislature", name=name, district="Hamilton", role="Mayor")
        p.add_source(MAYOR_PAGE)

        main = page.xpath("//main") or page.xpath("//body")
        phone = self.get_phone(main[0], area_codes=[289, 365, 905], error=False)
        if phone:
            p.add_contact("voice", phone, "legislature")
        image = [
            src
            for src in main[0].xpath(".//img/@src")
            if re.search(r"[Mm]ayor", src) and not re.search(r"social", src)
        ]
        if image:
            p.image = image[0]

        return p
