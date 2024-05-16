import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.city.kawarthalakes.on.ca/city-hall/mayor-council/members-of-council"


class KawarthaLakesPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//p[@class="WSIndent"]/a')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = re.findall(r"(Ward [0-9]{1,2})", councillor.text_content())
            if district:
                district = district[0]
                name = councillor.text_content().replace(district, "").strip()
                role = "Councillor"
            else:
                district = "Kawartha Lakes"
                name = councillor.text_content().replace("Mayor", "").strip()
                role = "Mayor"

            url = councillor.attrib["href"]
            page = self.lxmlize(url)
            email = self.get_email(page)
            image = page.xpath('//img[@class="image-right"]/@src')[0]

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            p.add_contact("email", email)
            p.image = image
            yield p
