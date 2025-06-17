import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.edmonton.ca/city_government/city_organization/city-councillors"
MAYOR_PAGE = "https://www.edmonton.ca/city_government/city_organization/the-mayor"
MAYOR_CONTACT_PAGE = "https://www.edmonton.ca/city_government/city_organization/mayor/contact-the-mayor"


class EdmontonPersonScraper(CanadianScraper):
    def get_contact_info(self, page, p: Person):
        contacts = page.xpath('//table[@summary="Contact information"]//tr')
        for contact in contacts:
            contact_type = contact.xpath("./th/text()")[0]
            value = contact.xpath("./td")[0].text_content().strip()
            if "Title" in contact_type:
                continue
            if "Website" in contact_type or "Facebook" in contact_type or "Twitter" in contact_type:
                value = contact.xpath("./td/a/text()")[0]
                p.add_link(value)
            elif "Telephone" in contact_type or "Phone" in contact_type:
                p.add_contact("voice", value, "legislature")
            elif "Fax" in contact_type:
                p.add_contact("fax", value, "legislature")
            elif "Email" in contact_type:
                p.add_contact("email", value)

    def scrape(self):
        yield self.scrape_mayor()
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('.//div[contains(@class, "feature-box__title")]')
        assert len(councillors), "No councillors found"
        for cell in councillors:
            name = cell.xpath("./a")[0].text_content()
            if "Vacant" in name:
                continue

            page_url = cell.xpath("./a/@href")[0]
            page = self.lxmlize(page_url)
            district_name = page.xpath(
                '//h1[contains(@class, "page-title")]|//h1[contains(@class, "page-title page-title--black-content-page")]'
            )[0].text_content()
            district, name = district_name.split(" - ", 1)
            district = district.replace("Ward ", "")
            if " " in district and re.search("[^A-Za-z ]", district):
                district = district.split()[0]

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.add_source(COUNCIL_PAGE)
            p.add_source(page_url)

            image = page.xpath('//div[contains(@class, "content")]//img/@src')
            if image:
                p.image = image[0]

            address = page.xpath("//address//p")
            if address:
                address = address[0].text_content()
                p.add_contact("address", address, "legislature")
            self.get_contact_info(page, p)
            yield p

    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)
        name = page.xpath('//h1[contains(text(), "Mayor")]/text()')[0].replace("Mayor", "").strip()

        p = Person(primary_org="legislature", name=name, district="Edmonton", role="Mayor")
        p.add_source(MAYOR_PAGE)

        contact_page = self.lxmlize(MAYOR_CONTACT_PAGE)

        address = " ".join(contact_page.xpath("//address/p/text()"))
        p.add_contact("address", address, "legislature")

        self.get_contact_info(contact_page, p)

        return p
