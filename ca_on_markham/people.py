import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = (
    "https://www.markham.ca/wps/portal/home/about/city-hall/regional-ward-councillors/02-regional-ward-councillors"
)
MAYOR_PAGE = "https://www.markham.ca/wps/portal/home/about/city-hall/mayor/00-mayors-office"


class MarkhamPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor(MAYOR_PAGE)

        councillors = page.xpath('//div[@class="col-sm-3 col-xs-6"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name, district = councillor.xpath(".//h4/text()")[0].split(", ")
            if "Ward" in district:
                district = district.replace("Councillor", "").strip()
                role = "Councillor"
            elif "Regional" in district:
                role = "Regional Councillor"
                district = f"Markham (seat {regional_councillor_seat_number})"
                regional_councillor_seat_number += 1
            else:
                role = district
                district = "Markham"

            image = councillor.xpath(".//img/@src")[0]
            url = "https://www.markham.ca/wps/portal/home/about" + re.search(
                r"(?<=about).*(?='\))", councillor.xpath(".//a/@href")[0]
            ).group(0)

            address, phone, email, links = self.get_contact(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = image
            p.add_contact("address", address, "legislature")
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)

            for link in links:
                p.add_link(link)

            yield p

    def get_contact(self, url):
        page = self.lxmlize(url)

        contact_node = page.xpath('//div[@class="vcard col-sm-6"]')[0]
        links = []

        address = contact_node.xpath(".//p/text()")[:2]
        links = get_links(contact_node)
        phone = self.get_phone(contact_node)
        email = self.get_email(contact_node)

        return address, phone, email, links

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('//img/@alt[contains(., "Mayor")]')[0].split(", ", 1)[1]
        email = self.get_email(page)
        phone = self.get_phone(page)

        p = Person(primary_org="legislature", name=name, district="Markham", role="Mayor")
        p.image = page.xpath('//img[contains(./@alt, "Mayor")]/@src')[0]
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_source(url)

        yield p


def get_links(elem):
    links_r = []
    links = elem.xpath(".//a")
    for link in links:
        link = link.attrib["href"]
        if "http://www.markham.ca" not in link and "mail" not in link:
            links_r.append(link)
    return links_r
