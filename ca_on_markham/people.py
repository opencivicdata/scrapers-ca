from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.markham.ca/about-city-markham/city-hall/regional-ward-councillors"
MAYOR_PAGE = "https://www.markham.ca/about-city-markham/city-hall/mayors-office"


class MarkhamPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        yield from self.scrape_mayor(MAYOR_PAGE)

        councillors = page.xpath('//div[contains(@class, "information-card")][.//h3]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name = councillor.xpath("normalize-space(.//h3)")
            if "Vacant" in name:
                continue
            district = councillor.xpath("normalize-space(.//p)")

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

            url = councillor.xpath(".//a/@href")[0]

            address, phone, email, links = self.get_contact(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            image = councillor.xpath(".//img/@src")
            if image:
                p.image = image[0]
            if address:
                p.add_contact("address", address, "legislature")
            if phone:
                p.add_contact("voice", phone, "legislature")
            if email:
                p.add_contact("email", email)

            for link in links:
                p.add_link(link)

            yield p

    def get_contact(self, url):
        page = self.lxmlize(url)

        contact_node = page.xpath(
            '//div[contains(@class, "committee-right-info-section") or contains(@class, "field-content--name--body")]'
        )
        contact_node = contact_node[0] if contact_node else page

        address_parts = [
            contact_node.xpath(f'normalize-space(.//span[contains(@class, "{class_name}")])')
            for class_name in ("address-line1", "locality", "administrative-area", "postal-code", "country")
        ]
        address_parts = [part for part in address_parts if part]
        address = " ".join(address_parts)

        links = get_links(contact_node)
        phone = self.get_phone(contact_node, error=False)
        email = self.get_email(contact_node, error=False)

        return address, phone, email, links

    def scrape_mayor(self, url):
        page = self.lxmlize(url)
        name = page.xpath('.//div[contains(@class, "field-content--name--body")]/h2/text()')
        if not name:
            name = page.xpath('.//h1/text()|.//h2[not(contains(@class, "field-label"))]/text()')
        name = [
            n.strip()
            for n in name
            if n.strip()
            and "Office" not in n
            and "Request" not in n
            and "Contact" not in n
            and "News" not in n
            and "Meeting" not in n
            and "Connect" not in n
        ][0]

        contact_node = page.xpath('.//div[contains(@class, "dept-contact-info--block")]')
        if contact_node:
            contact_node = contact_node[0]
        else:
            contact_node = page

        email = self.get_email(contact_node, error=False)
        phone = self.get_phone(contact_node, error=False)

        p = Person(primary_org="legislature", name=name, district="Markham", role="Mayor")
        images = page.xpath(
            './/div[contains(@class, "media--image")]//img/@src|.//img[contains(@src, "/files/")]/@src'
        )
        if images:
            p.image = images[0]
        if email:
            p.add_contact("email", email)
        if phone:
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
