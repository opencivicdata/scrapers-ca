from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.haldimandcounty.ca/council-information/council-members/"


class HaldimandCountyPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//a[@class="lsvr_person-list-widget__item-title-link"]/@href')
        assert len(councillors), "No councillors found"
        for url in councillors:
            page = self.lxmlize(url)
            name = page.xpath("//h1")[0].text_content()
            if "Mayor" in page.xpath('//p[@class="main__subtitle"]')[0].text_content():
                district = "Haldimand County"
                role = "Mayor"
            else:
                role, district = page.xpath('//p[@class="main__subtitle"]')[0].text_content().split(" - ")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)

            p.image = page.xpath('//p[@class="post__thumbnail"]/noscript//@src')[0]
            email = self.get_email(page)
            phone = self.get_phone(page)
            p.add_contact("email", email)
            p.add_contact("voice", phone, "legislature")

            yield p
