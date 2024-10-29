import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.newwestcity.ca/city_hall/mayor_and_council/councillors.php"
MAYOR_PAGE = "https://www.newwestcity.ca/city_hall/mayor_and_council/mayor.php"


class NewWestminsterPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        seat_number = 1
        councillors = page.xpath('//div[@id="main-bottom"]//li')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//a[@name]")[0].text_content()
            district = f"New Westminster (seat {seat_number})"
            seat_number += 1
            p = Person(primary_org="legislature", name=name, role="Councillor", district=district)
            photo = councillor.xpath("//img/@src")[0]
            email_parts = re.sub(r"[\"\[\]]", "", councillor.xpath('//div[@class="text"]//a/@data-ob')[0])
            email = "@".join(email_parts.split(",")[:2])
            phone = self.get_phone(councillor)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.image = photo
            yield p
        page = self.lxmlize(MAYOR_PAGE)
        name = page.xpath('//p[@class="page_description"]/strong')[0].text_content()
        email_parts = re.sub(r"[\"\[\]]", "", page.xpath("//a/@data-ob")[0])
        email = "@".join(email_parts.split(",")[:2])
        phone = self.get_phone(page)

        p = Person(primary_org="legislature", name=name, role="Mayor", district="New Westminster")
        p.add_source(MAYOR_PAGE)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        yield p
