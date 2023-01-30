from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.mississauga.ca/portal/cityhall/mayorandcouncil"
MAYOR_PAGE = "http://www.mississauga.ca/portal/cityhall/mayorsoffice"
CONTACT_PAGE = "http://www.mississauga.ca/portal/helpfeedback/contactus"


class MississaugaPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//li/a[contains(@href, "ward")]')
        assert len(councillors), "No councillors found"
        for councillor_url in councillors:
            if "Vacant" not in councillor_url.xpath("./following-sibling::div[2]/text()")[0]:
                yield self.councillor_data(councillor_url.attrib["href"])

        yield self.mayor_data(MAYOR_PAGE)

    def councillor_data(self, url):
        page = self.lxmlize(url)

        name = page.xpath("//table//strong/text()")[0]
        district = page.xpath('//span[@class="pageHeader"]//text()')[0]
        email = self.get_email(page, '//div[@class="blockcontentclear"]')
        photo = page.xpath('//div[@class="blockcontentclear"]//img[1]/@src')[0]

        p = Person(primary_org="legislature", name=name, district=district, role="Councillor")
        p.add_source(COUNCIL_PAGE)
        p.add_source(url)
        p.add_contact("email", email)
        p.image = photo

        return p

    def mayor_data(self, url):
        page = self.lxmlize(url)

        name_text = page.xpath('//p/*[contains(.//text(), "Mayor")]/text()')[0]
        name = name_text.split(",")[0]
        photo = page.xpath('//img[contains(@src, "mayor")]/@src')[0]

        p = Person(primary_org="legislature", name=name, district="Mississauga", role="Mayor")
        p.add_source(url)
        p.add_source(CONTACT_PAGE)
        p.add_contact("email", "mayor@mississauga.ca")  # hardcoded
        p.image = photo

        return p
