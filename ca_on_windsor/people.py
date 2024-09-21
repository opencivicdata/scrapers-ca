import json

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.citywindsor.ca/mayor-and-council"


class WindsorPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)
        data_url = page.xpath('//comment()[contains(., "SITE JS")]/following-sibling::script/@src')[0]
        data = json.loads(self.get(data_url).text.split(" = ")[1])
        nav_items = []
        for item in data:
            if item["RollupType"] == "SidebarNavigation":
                nav_items = item["RollupFields"]
        for item in nav_items:
            if item["Title"].startswith("Mayor") and item["Parent"] == "Mayor and City Council":
                mayor_url = "https://www.citywindsor.ca" + item["RelativeURL"]
            if "Councillors" in item["Title"]:
                councillors_url = "https://www.citywindsor.ca" + item["RelativeURL"]

        page = self.lxmlize(councillors_url, user_agent="Mozilla/5.0")
        councillors = page.xpath("//h2")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district, name = councillor.text_content().split(" – ")
            image = councillor.xpath("./preceding-sibling::img/@src")[0]
            contact_node = councillor.xpath("./following-sibling::p")[0]
            phone = self.get_phone(contact_node)
            email = self.get_email(contact_node)
            url = contact_node.xpath('.//@href[not(contains(., "mailto:"))]')[0]

            p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
            p.image = image
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            yield p

        page = self.lxmlize(mayor_url)
        title = page.xpath("//h1")[0].text_content()
        name = title.replace("Mayor ", "")
        image = page.xpath('//img[contains(./@alt, "Mayor")]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Windsor", role="Mayor", image=image)
        p.add_source(mayor_url)

        yield p
