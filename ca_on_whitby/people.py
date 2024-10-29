from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.whitby.ca/en/town-hall/mayor-and-council.aspx"


class WhitbyPersonScraper(CanadianScraper):
    def scrape(self):
        regional_councillor_seat_number = 1
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//table[@class="icrtAccordion"]//tr[contains(./td/@data-name, "accParent")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath("./td")[0].text_content().strip().replace("\xa0", " ")
            node = councillor.xpath("./following-sibling::tr/td")[0]

            if "Mayor" in name:
                role = "Mayor"
                district = "Whitby"
                name = name.replace("Mayor ", "")
            else:
                name, role = name.split(", ")
                if role == "Regional Councillor":
                    district = f"Whitby (seat {regional_councillor_seat_number})"
                    regional_councillor_seat_number += 1
                else:
                    district = role.split(" – ")[1]
                    district = " ".join(district.split(" ")[:2])
                    role = "Councillor"

            image = node.xpath(".//img/@src")[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", self.get_phone(node), "legislature")
            p.image = image

            yield p
