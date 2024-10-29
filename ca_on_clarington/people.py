import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.clarington.net/en/town-hall/Meet-Your-Councillors.aspx"
MAYOR_PAGE = "https://www.clarington.net/en/town-hall/mayor.aspx"


class ClaringtonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath("//td[@data-name='accParent']")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name, role_district = councillor.text_content().split(" - ")
            role, district = re.split(r"(?<=Councillor) ", role_district, maxsplit=1)
            content_node = councillor.xpath("../following-sibling::tr")[0]
            email = self.get_email(content_node)
            photo_url = content_node.xpath(".//img/@src")[0]
            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("email", email)
            yield p

        page = self.lxmlize(MAYOR_PAGE).xpath('//div[@id="mainContent"]')[0]
        name = page.xpath(".//img/@alt")[0].replace("Mayor", "").strip()
        photo_url = page.xpath(".//img/@src")[0]
        email = self.get_email(page)

        p = Person(primary_org="legislature", name=name, district="Clarington", role="Mayor", image=photo_url)
        p.add_contact("email", email)
        p.add_source(MAYOR_PAGE)
        yield p
