from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.lambtononline.ca/en/county-government/councillors.aspx"


class LambtonPersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//tbody//td[@data-name="accParent"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            text = councillor.xpath(".//h3/text()")[0]
            if "Deputy Warden" in text:
                role = "Deputy Warden"
                name = text.replace("Deputy Warden ", "")
                district = "Lambton"
            elif "Warden" in text:
                role = "Warden"
                name = text.replace("Warden ", "")
                district = "Lambton"
            else:
                role = "Councillor"
                name = text.replace("Councillor ", "")
                district = f"Lambton (seat {councillor_seat_number})"
                councillor_seat_number += 1

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath("../following-sibling::tr//img/@src")[0]
            p.add_contact("voice", self.get_phone(councillor.xpath("../following-sibling::tr")[0]), "legislature")

            yield p
