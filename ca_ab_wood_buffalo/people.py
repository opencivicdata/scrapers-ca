from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.rmwb.ca/en/mayor-council-and-administration/councillors.aspx"
MAYOR_PAGE = "https://www.rmwb.ca/en/mayor-council-and-administration/mayor.aspx"


class WoodBuffaloPersonScraper(CanadianScraper):
    def scrape_mayor(self):
        page = self.lxmlize(MAYOR_PAGE)
        paragraph = page.xpath("//div[@id='StandardOneColumnTK1_lm176']/p/text()")[0]
        name = " ".join(paragraph.strip().split()[0:2])
        image = page.xpath("//div[@id='mainContent']//@src")[0]

        p = Person(primary_org="legislature", name=name, district="Wood Buffalo", role="Mayor")
        p.add_source(MAYOR_PAGE)

        p.image = image

        return p

    def scrape(self):
        seat_numbers = defaultdict(int)

        page = self.lxmlize(COUNCIL_PAGE)

        yield self.scrape_mayor()

        wards = page.xpath("//div[@id='StandardOneColumnTK1_lm175']//h2")
        assert len(wards), "No wards found"
        for ward in wards:
            area = ward.text_content().split("–", 1)[1].strip()
            councillors = ward.xpath("./following-sibling::table[1]/tbody/tr/td/h3")
            assert len(councillors), f"No councillors found for {area}"
            for councillor in councillors:
                name = councillor.text_content()

                if area in ("Ward 1", "Ward 2"):
                    seat_numbers[area] += 1
                    district = f"{area} (seat {seat_numbers[area]})"
                else:
                    district = area

                p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
                p.add_source(COUNCIL_PAGE)

                p.image = councillor.xpath("../../following-sibling::*//img/@src")[0]

                email_node = councillor.xpath("../../following-sibling::*[1]//p/a/@href")
                if email_node:
                    email = email_node[0].split(":", 1)[1]
                    p.add_contact("email", email)

                yield p
