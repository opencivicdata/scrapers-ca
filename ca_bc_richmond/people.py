from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.richmond.ca/city-hall/city-council.htm"


class RichmondPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        urls = page.xpath('//a[@class="ipf-sitemap-tr-level2"]/@href')
        assert len(urls), "No councillors found"
        for url in urls:
            page = self.lxmlize(url)
            role, name = page.xpath("//h1//text()")[0].split(" ", 1)
            photo_url = page.xpath('//img[@class="float-right"]/@src')[0]
            email = self.get_email(page)
            phone = self.get_phone(page)

            if role == "Mayor":
                district = "Richmond"
            else:
                district = f"Richmond (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = photo_url
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            yield p
