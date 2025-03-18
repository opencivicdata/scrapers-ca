from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.vaughan.ca/council"


class VaughanPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="city-table-responsive"]//a[@title][contains(./@href, "council")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            url = councillor.xpath("./@href")[0]
            page = self.lxmlize(url)
            title = page.xpath("//h1/span")[0].text_content()
            if "-" in title:
                district, name = title.split("-")
            else:
                district, name = title.split("Councillor")
            if "Regional" in district:
                role = "Regional Councillor"
                district = f"Vaughan (seat {regional_councillor_seat_number})"
                regional_councillor_seat_number += 1
            elif "Ward" in district:
                role = "Councillor"
                district = district.strip()
            else:
                role = "Mayor"
                district = "Vaughan"
            name = name.strip()

            email_node = page.xpath('//div[@class="field-container label-display--inline field-name--field_email"]')
            phone_node = page.xpath(
                '//div[@class="field-container label-display--inline field-name--field_phone_number"]'
            )
            fax_node = page.xpath('//div[@class="field-container label-display--inline field-name--field_fax_number"]')

            p = Person(primary_org="legislature", name=name, district=district.strip(), role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            if role == "Mayor":
                contact_info = page.xpath('//p[contains(.,"Tel:")]/text()')
                phone = contact_info[0].split(": ")[1]
                fax = contact_info[1].split(": ")[1]
                email = contact_info[2].replace("\u200b", "")
                p.add_contact("email", email)
                p.add_contact("voice", phone, "legislature")
                p.add_contact("fax", fax, "legislature")

            if phone_node:
                self.get_phone(phone_node[0]).replace("=", "")
                p.add_contact("voice", phone, "legislature")
            if fax_node:
                p.add_contact("fax", self.get_phone(fax_node[0]), "legislature")
            if email_node:
                p.add_contact("email", self.get_email(email_node[0]))

            image = councillor.xpath("./ancestor::td//@src")
            if image:
                p.image = image[0]

            if page.xpath('.//a[contains(@href,"facebook")]'):
                p.add_link(page.xpath('.//a[contains(@href,"facebook")]')[0].attrib["href"])
            if page.xpath('.//a[contains(@href,"twitter")]'):
                p.add_link(page.xpath('.//a[contains(@href,"twitter")]')[0].attrib["href"])
            if page.xpath('.//a[contains(@href,"youtube")]'):
                p.add_link(page.xpath('.//a[contains(@href, "youtube")]')[0].attrib["href"])
            yield p
