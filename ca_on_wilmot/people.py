from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.wilmot.ca/Modules/contact/search.aspx?s=EFHOVXSi8AOIMKMStZMNvAeQuAleQuAl"


class WilmotPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="contactList"]//tr')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name, role_district = councillor.xpath(".//button/text()")[0].split(" - ", 1)
            if "Mayor" in role_district:
                yield scrape_mayor(councillor, name)
                continue
            role, district = role_district.split(" - ")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            phone = self.get_phone(councillor).replace("/", "")
            p.add_contact("voice", phone, "legislature")
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
