import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.grimsby.ca/en/town-hall/council.aspx"
MAYOR_PAGE = "https://www.grimsby.ca/en/town-hall/about-the-mayor.aspx"


class GrimsbyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        wards = page.xpath("//p[@class='tab ']")
        assert len(wards), "No wards found"

        for ward in wards:
            area = ward.xpath(".//a")[0].text_content().strip()
            councillors_node = ward.xpath("./following-sibling::div")[0]

            for i in range(2):
                name_node = councillors_node.xpath(
                    './/h5[contains(./strong, "Councillor")]|.//h5[contains(., "Councillor")]'
                )[i]
                name = re.split(r"\s", name_node.text_content(), maxsplit=1)[1]
                district = f"{area} (seat {i + 1})"
                phone = self.get_phone(name_node.xpath('./following-sibling::*[contains(., "Phone")]')[0])
                email = self.get_email(name_node.xpath("./following-sibling::p[contains(., 'Email')]")[0])
                image = councillors_node.xpath(".//@src")[i]

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor", image=image)
                p.add_contact("email", email)
                p.add_contact("voice", phone, "legislature")
                p.add_source(COUNCIL_PAGE)

                yield p

        page = self.lxmlize(MAYOR_PAGE)
        role, name = page.xpath("//h3")[0].text_content().split(" ", 1)

        email = self.get_email(page)
        phone = self.get_phone(page.xpath("//div[contains(@class, 'left')]//p[contains(., '905')]")[0])
        image = page.xpath("//p//@src")[0]

        p = Person(primary_org="legislature", name=name, district="Grimsby", role=role, image=image)
        p.add_contact("email", email)
        p.add_contact("voice", phone, "legislature")
        p.add_source(MAYOR_PAGE)

        yield p
