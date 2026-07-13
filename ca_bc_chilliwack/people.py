from urllib.parse import urljoin

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.chilliwack.com/main/page.cfm?id=2257"


class ChilliwackPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        member_links = page.xpath('//ul[@id="navtree"]//a[@class="subpage"]/@href')
        assert len(member_links) == 7, "Expected 7 council members"

        councillor_seat_number = 1
        for index, href in enumerate(member_links):
            url = urljoin(COUNCIL_PAGE, href)
            member_page = self.lxmlize(url)

            name = member_page.xpath('normalize-space(//span[@id="contentPageTitle"])')
            if index == 0:
                role = "Mayor"
                district = "Chilliwack"
            else:
                role = "Councillor"
                district = f"Chilliwack (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = member_page.xpath('//div[@id="pageContent"]//img/@src')
            if image:
                p.image = urljoin(url, image[0])

            yield p
