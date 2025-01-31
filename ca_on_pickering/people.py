import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.pickering.ca/en/city-hall/citycouncil.aspx"


class PickeringPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_contacts = []
        council_contacts = []

        mayor_phone = page.xpath("//strong[contains(text(), 'Office of the Mayor')]/following-sibling::text()[contains(., 'T.')][1]")[0]
        mayor_phone = page.xpath("//strong[contains(text(), 'Office of the Mayor')]/following-sibling::text()[contains(., 'T.')][1]")[0]
        mayor_phone = re.findall(r"\b\d{3}\.\d{3}\.\d{4}\b", mayor_phone)[0]
        mayor_phone = mayor_phone.replace(".", "-")
        
        mayor_fax = page.xpath("//strong[contains(text(), 'Office of the Mayor')]/following-sibling::text()[contains(., 'F.')][1]")[0]
        mayor_fax = re.findall(r"\b\d{3}\.\d{3}\.\d{4}\b", mayor_fax)[0]
        mayor_fax = mayor_fax.replace(".", "-")
        
        mayor_contacts.append(mayor_phone)
        mayor_contacts.append(mayor_fax)

        council_phone = page.xpath("//strong[contains(text(), 'Council Office')]/following-sibling::text()[contains(., 'T.')][1]")[0]
        council_phone = page.xpath("//strong[contains(text(), 'Council Office')]/following-sibling::text()[contains(., 'T.')][1]")[0]
        council_phone = re.findall(r"\b\d{3}\.\d{3}\.\d{4}\b", council_phone)[0]
        council_phone = council_phone.replace(".", "-")
        
        council_fax = page.xpath("//strong[contains(text(), 'Office of the Mayor')]/following-sibling::text()[contains(., 'F.')][1]")[0]
        council_fax = re.findall(r"\b\d{3}\.\d{3}\.\d{4}\b", council_fax)[0]
        council_fax = council_fax.replace(".", "-")
        
        council_contacts.append(council_phone)
        council_contacts.append(council_fax)
        
        councillors = page.xpath('//div[@class="inner  "]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//strong//text()")[0]

            if "Councillor" in name:
                name = name.replace("Councillor", "").strip()
                role_ward = councillor.xpath(".//text()")[10]
                role, ward = re.split(r"\s(?=Ward)", role_ward, maxsplit=1)
            else:
                name = name.replace("Mayor", "")
                role = "Mayor"
                ward = "Pickering"

            email = self.get_email(councillor)
            p = Person(primary_org="legislature", name=name, district=ward, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            p.image = councillor.xpath(".//img/@src")[0]

            links = councillor.xpath(".//a")
            for link in links:
                if "@" in link.text_content():
                    continue
                if "Profile" in link.text_content():
                    p.add_source(link.attrib["href"])
                else:
                    p.add_link(link.attrib["href"])

            if role == "Mayor":
                add_contacts(p, mayor_contacts)
            else:
                add_contacts(p, council_contacts)
            yield p


def add_contacts(p, contacts):
    phone = re.findall(r"[0-9]{3}\-[0-9]{3}\-[0-9]{4}", contacts[0])[0]
    fax = re.findall(r"[0-9]{3}\-[0-9]{3}\-[0-9]{4}", contacts[1])[0]
    p.add_contact("voice", phone, "legislature")
    p.add_contact("fax", fax, "legislature")

