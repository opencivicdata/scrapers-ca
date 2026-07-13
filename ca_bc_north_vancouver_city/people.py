from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.cnv.org/City-Hall/Mayor-Council"


class NorthVancouverCityPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        urls = []
        for href in page.xpath(
            '//a[contains(@href, "/City-Hall/Mayor-Council/Mayor-") '
            'or contains(@href, "/City-Hall/Mayor-Council/Councillor-")]/@href'
        ):
            url = urljoin(COUNCIL_PAGE, href)
            if url not in urls and all(part not in url for part in ["/Community-Updates", "/Invite-", "/Request-"]):
                urls.append(url)
        assert len(urls) == 7, "Expected 7 council profiles"

        councillor_seat_number = 1
        for url in urls:
            profile_page = self.lxmlize(url)
            title = profile_page.xpath("normalize-space(//h1)")

            if title.startswith("Mayor "):
                role = "Mayor"
                name = title.replace("Mayor ", "", 1)
                district = "North Vancouver"
            else:
                role = "Councillor"
                name = title.replace("Councillor ", "", 1)
                district = f"North Vancouver (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = profile_page.xpath('//img[contains(@src, "/Images/Mayor-and-Council/Photos/")]/@src')
            if image:
                p.image = urljoin(url, image[0])

            email = self.get_email(profile_page, error=False)
            if email:
                p.add_contact("email", email)

            phone = self.get_phone(profile_page, area_codes=[236, 604, 672, 778], error=False)
            if phone:
                p.add_contact("voice", phone, "legislature")

            yield p
