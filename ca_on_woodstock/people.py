from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.cityofwoodstock.ca/your-government/mayor-and-council/"


class WoodstockPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        h3_nodes = page.xpath('//div[contains(@class,"text base-text")]/h3')
        assert h3_nodes, "No council member headings found"

        seat = 0
        for h3 in h3_nodes:
            name = h3.text_content().strip()
            name = name.split(" (", 1)[0].strip()
            if not name:
                continue

            preceding_h2 = h3.xpath("preceding::h2[1]")
            role_text = preceding_h2[0].text_content().strip() if preceding_h2 else ""

            if role_text == "Mayor":
                role = "Mayor"
                district = "Woodstock"
            elif "Councillor" in role_text:
                seat += 1
                role = "Councillor"
                district = f"Woodstock (seat {seat})"
            else:
                continue

            block = h3.getparent()
            phone = self.get_phone(block, area_codes=[519, 226, 548], error=False)
            image = block.xpath(".//img/@src")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if image:
                p.image = image[0]
            yield p
