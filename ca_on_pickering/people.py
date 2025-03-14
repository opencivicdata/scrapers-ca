import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.pickering.ca/en/city-hall/citycouncil.aspx"


class PickeringPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        mayor_contacts = page.xpath("//table[1]//tr/td[1]/text()")
        council_contacts = page.xpath("//table[1]//tr/td[2]/text()")

        councillors = page.xpath('//div[@class="lmColumn ui-sortable fbg-col-xs-12 fbg-col-sm-4 column"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//strong//text()")[0]

            if "Councillor" in name:
                name = name.replace("Councillor", "").strip()
                role_ward = councillor.xpath(".//text()")[1]
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
    phone = re.findall(r"[0-9]{3}\.[0-9]{3}\.[0-9]{4}", contacts[0])[0]
    fax = re.findall(r"[0-9]{3}\.[0-9]{3}\.[0-9]{4}", contacts[1])[0]
    p.add_contact("voice", phone, "legislature")
    p.add_contact("fax", fax, "legislature")
