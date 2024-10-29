import re
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.belleville.ca/en/city-hall/councillors.aspx"
MAYOR_PAGE = "https://www.belleville.ca/en/city-hall/mayors-office.aspx"


class BellevillePersonScraper(CanadianScraper):
    seat_numbers = defaultdict(int)

    def scrape(self):
        page = self.lxmlize(MAYOR_PAGE)

        node = page.xpath("//tbody/tr")[0]
        name = node.xpath("./td")[0].text_content()
        phone = node.xpath("./td")[2].text_content()
        email = self.get_email(node)
        image = page.xpath('//div[@class = "iCreateDynaToken"]//img/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Belleville", role="Mayor")
        p.add_source(MAYOR_PAGE)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("email", email)
        p.image = image

        yield p

        page = self.lxmlize(COUNCIL_PAGE)
        wards = page.xpath('//h2[contains(text(), "Councillors")]')
        assert len(wards), "No councillors found"
        for ward in wards:
            ward_name = re.search(r"(Ward.+) Councillors", ward.text).group(1)
            councillors = ward.xpath("./following-sibling::*[img]")
            for councillor in councillors:
                self.seat_numbers[ward_name] += 1
                district = f"{ward_name} (seat {self.seat_numbers[ward_name]})"
                role = "Councillor"

                name = councillor.xpath("./following-sibling::p")[0].text_content()
                phone = councillor.xpath("./following-sibling::p/text()")[2].split(":")[1]
                email = councillor.xpath("./following-sibling::p/a//text()")[0]
                image = councillor.xpath("./img/@src")[0]

                p = Person(primary_org="legislature", name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_contact("voice", phone, "legislature")
                p.add_contact("email", email)
                p.image = image

                yield p
                if self.seat_numbers[ward_name] >= 6:  # Assigning councillors to correct Ward
                    break
