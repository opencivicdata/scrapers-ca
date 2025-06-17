import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.pickering.ca/en/city-hall/citycouncil.aspx"


class PickeringPersonScraper(CanadianScraper):
    def _create_person(self, *, element, name, district, role, phone_text, fax_text):
        p = Person(primary_org="legislature", name=name, district=district, role=role)
        p.add_source(COUNCIL_PAGE)
        p.add_contact("email", self.get_email(element))
        p.image = element.xpath(".//img/@src")[0]

        links = element.xpath(".//a")
        for link in links:
            if "@" in link.text_content():
                continue
            if "Profile" in link.text_content():
                p.add_source(link.attrib["href"])
            else:
                p.add_link(link.attrib["href"])

        for contact_type, letter, contact_text in (("voice", "T", phone_text), ("fax", "F", fax_text)):
            text = element.xpath(
                f"//strong[contains(text(), '{contact_text}')]/following-sibling::text()[contains(., '{letter}.')][1]"
            )[0]
            number = re.findall(r"\b\d{3}\.\d{3}\.\d{4}\b", text)[0].replace(".", "-")
            p.add_contact(contact_type, number, "legislature")

        return p

    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor = page.xpath('//div[contains(@class, "component-outro")]')[0]
        yield self._create_person(
            element=mayor,
            name=mayor.xpath(".//strong/text()")[0],
            district="Pickering",
            role="Mayor",
            phone_text="Office of the Mayor",
            fax_text="Office of the Mayor",
        )

        councillors = page.xpath('//div[@class="inner  "]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, ward = re.split(r"\s(?=Ward)", councillor.xpath(".//text()")[10], maxsplit=1)

            yield self._create_person(
                element=councillor,
                name=councillor.xpath(".//strong//text()")[0].replace("Councillor", "").strip(),
                district=ward,
                role=role,
                phone_text="Council Office",
                fax_text="Office of the Mayor",  # same as mayor
            )
