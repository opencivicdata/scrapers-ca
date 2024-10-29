from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://terrebonne.ca/membres-du-conseil-municipal/"


class TerrebonnePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, "utf-8")
        councillors = page.xpath('//div[contains(@class, "member-card jsBlockLink")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//a[@class="name"]/text()')[0]
            district = councillor.xpath('.//p[@class="district"]/text()')[0]
            if "Maire" in district:
                role = "Maire"
                district = "Terrebonne"
            else:
                role = "Conseiller"
                district = district.split(" - ")[0]

            photo_url = councillor.xpath(".//noscript/img/@src")[0]
            url = councillor.xpath(".//@href")[0]

            page = self.lxmlize(url)
            email = self.get_email(page)
            phone = self.get_phone(page)

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=photo_url)
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", phone, "legislature")
            p.add_contact("email", email)
            yield p
