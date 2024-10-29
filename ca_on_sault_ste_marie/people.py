import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://saultstemarie.ca/Government/City-Council.aspx"


class SaultSteMariePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        seat_numbers = defaultdict(int)

        councillors = page.xpath('//div[@class="mb-2"]//@href')
        assert len(councillors), "No councillors found"

        for link in councillors:
            page = self.lxmlize(link)
            title = page.xpath("//h1")[0].text_content()
            if "Mayor" in title:
                role = "Mayor"
                name = title.replace("Mayor ", "")
                district = "Sault Ste. Marie"
                image = None  # No image on the Mayor's page at the moment
                contact_node = page.xpath('//div[@id="mainContent_contactUs"]')[0]
                phone_numbers = re.findall(r"\d{3}-\d{3}-\d{4}", contact_node.text_content())
                phone = phone_numbers[0]
                fax = phone_numbers[1]
            else:
                role = "Councillor"
                area, name = title.split(" Councillor ")
                seat_numbers[area] += 1
                district = f"{area} (seat {seat_numbers[area]})"
                image = page.xpath(".//h3/img/@src")[0]
                contact_node = page.xpath('//div[@id="mainContent_left"]')[0]
                phone = self.get_phone(contact_node)
            email = self.get_email(contact_node)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            if image:
                p.image = image
            if fax:
                p.add_contact("fax", fax, "legislature")
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.add_source(link)
            yield p
