import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.lasalle.ca/en/town-hall/town-of-lasalle-council.aspx"


class LaSallePersonScraper(CanadianScraper):
    def scrape(self):
        councillor_seat_number = 1

        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="fbg-row lb-imageBox cm-datacontainer"]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            role, name = re.split(
                r"(?<=Mayor)|(?<=Councillor)", councillor.xpath(".//a/div")[0].text_content(), maxsplit=1
            )
            district = "LaSalle" if "Mayor" in role else f"LaSalle (seat {councillor_seat_number})"
            image = councillor.xpath(".//img/@src")[0]
            voice = re.search(r"\d{3}-\d{3}-\d{4} ext. \d+", councillor.text_content())
            cell = re.search(r"\d{3}-\d{3}-\d{4}(?! ext)", councillor.text_content())

            p = Person(primary_org="legislature", name=name, role=role, district=district, image=image)
            p.add_source(COUNCIL_PAGE)
            if voice:
                p.add_contact("voice", voice.group(0), "legislature")
            if cell:
                p.add_contact("cell", cell.group(0), "legislature")

            yield p
