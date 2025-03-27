from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.markham.ca/about-city-markham/city-hall/regional-ward-councillors"
MAYOR_PAGE = "https://www.markham.ca/about-city-markham/city-hall/mayors-office"


class MarkhamPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor(MAYOR_PAGE)

        councillors = page.xpath(
            '//div[@class="grid md:grid-cols-2 grid-cols-1 lg:grid-cols-4 gap-4 scrollablec"]/div'
        )
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name = councillor.xpath(".//h3/text()")[0].strip()
            district = councillor.xpath(".//p/text()")[0].strip()

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
            url = councillor.xpath(".//a/@href")[0]

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

        contact_node = page.xpath(
            '//div[@class="pd-x-16 pd-y-32 bg-white committee-right-info-section layout__region layout__region--second"]'
        )[0]
        links = []

        if contact_node.xpath('.//span[@class="address-line1"]/text()'):
            address = " ".join(
                (
                    contact_node.xpath('.//span[@class="address-line1"]/text()')[0],
                    contact_node.xpath('.//span[@class="locality"]/text()')[0],
                    contact_node.xpath('.//span[@class="administrative-area"]/text()')[0],
                    contact_node.xpath('.//span[@class="postal-code"]/text()')[0],
                    contact_node.xpath('.//span[@class="country"]/text()')[0],
                )
            )
        else:
            contact_node = page.xpath(
                '//div[@class="formatted-text field-content field-content--label--body field-content--entity-type--block-content field-content--name--body"]'
            )[0]
            address = f"{contact_node.xpath('.//p/text()')[0]} {contact_node.xpath('.//p/text()')[1]}"

        links = get_links(contact_node)
        phone = self.get_phone(contact_node)
        email = self.get_email(contact_node)

        return address, phone, email, links

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath(
            './/div[@class="formatted-text field-content field-content--label--body field-content--entity-type--block-content field-content--name--body"]/h1/span/span/text()'
        )[0]
        contact_node = page.xpath('.//div[@class="dept-contact-info--block"]')[0]
        email = self.get_email(contact_node)
        phone = self.get_phone(contact_node)

        p = Person(primary_org="legislature", name=name, district="Markham", role="Mayor")
        p.image = page.xpath('.//div[@class="align-right media--image"]/div/img/@src')[0]
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_source(url)

        yield p


def get_links(elem):
    links_r = []
    links = elem.xpath(".//a")
    for link in links:
        link = link.attrib["href"]
        if "http://www.markham.ca" not in link and "mail" not in link and "tel" not in link:
            links_r.append(link)
    return links_r
