from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.whitby.ca/en/townhall/meetyourcouncil.asp?_mid_=11883"


class WhitbyPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//a[@title="Mayor and Council::Meet Your Council"]/following-sibling::ul//@href')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            node = self.lxmlize(councillor).xpath('//div[@id="printArea"]')[0]
            name = node.xpath(".//h1/text()")[0]

            if "Mayor" in name:
                role = "Mayor"
                district = "Whitby"
                name = name.replace("Mayor ", "")
            else:
                role = node.xpath(".//h2/text()")[0]
                if "Regional Councillor" in role:
                    district = "Whitby (seat {})".format(regional_councillor_seat_number)
                    regional_councillor_seat_number += 1
                else:
                    role, district = role.split(", ")
                    district = district.split(" (")[0]

            image = node.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", self.get_phone(node), "legislature")
            p.add_contact("email", self.get_email(node))
            p.image = image

            yield p
