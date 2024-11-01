from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.wilmot.ca/en/township-office/council.aspx"


class WilmotPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('.//table[@class="icrtAccordion"]//tr')
        assert len(councillors), "No councillors found"
        for i in range(0, len(councillors), 2):
            role_name, contact_info = councillors[i], councillors[i + 1]
            role, name = role_name.text_content().strip().replace("\xa0", " ").split("— ")

            if "Councillor" in role:
                district = role.split(" Councillor")[0]
                role = "Councillor"
            else:
                district = "Wilmot"

            phone = self.get_phone(contact_info)
            email = self.get_email(contact_info)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            yield p


def scrape_mayor(div, name):
    p = Person(primary_org="legislature", name=name, district="Wilmot", role="Mayor")
    p.add_source(COUNCIL_PAGE)

    address = div.xpath('.//div[@class="contactListAddress"]')[0].text_content()
    phone = div.xpath('.//div[@class="contactListMainNumber"]/a/text()')[0]
    other_phone = div.xpath('.//div[@class="contactListPhNumber"]/a/text()')[0]
    p.add_contact("address", address, "legislature")
    p.add_contact("voice", phone, "legislature")
    p.add_contact("voice", other_phone, "office")

    return p
