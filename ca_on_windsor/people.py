from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.citywindsor.ca/mayor-and-council/city-councillors"
MAYOR_PAGE = "https://www.citywindsor.ca/mayor-and-council/mayor-drew-dilkens"


class WindsorPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

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

        page = self.lxmlize(MAYOR_PAGE)
        title = page.xpath("//h1")[0].text_content()
        name = title.replace("Mayor ", "")
        image = page.xpath('//img[contains(./@alt, "Mayor")]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Windsor", role="Mayor", image=image)
        p.add_source(MAYOR_PAGE)

        yield p
