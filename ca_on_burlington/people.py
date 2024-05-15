from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.burlington.ca/en/council-and-city-administration/council-members-and-wards.aspx"
MAYOR_PAGE = "https://www.burlington.ca/en/council-and-city-administration/mayor.aspx"


class BurlingtonPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//a[contains(., "- Councillor")][@class="hasChildren mainNavItem  mainSiteNav"]/@href'
        )
        assert len(councillors), "No councillors found"
        for url in councillors:
            yield self.scrape_person(url)

        yield self.scrape_person(MAYOR_PAGE)

    def scrape_person(self, url):
        page = self.lxmlize(url)

        info = page.xpath("//h1")[0].text_content()
        if "Mayor" in info:
            role, name = info.split(" ", 1)
            name = name.split(" ", 1)[1]
            role = "Mayor"
            district = "Burlington"
        else:
            district, role_name = info.split(" - ", 1)
            role, name = role_name.split(" ", 1)

        contact_node = page.xpath('//div[@class="lb-imageBox_content"]')[1]
        phone = self.get_phone(contact_node)
        email = self.get_email(contact_node)
        image = page.xpath('//div[@class="iCreateNoneditableToken"]//img/@src')[0]

        p = Person(primary_org="legislature", name=name, role=role, district=district, image=image)
        p.add_contact("voice", phone, "legislature")
        p.add_contact("email", email)
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)

        return p
