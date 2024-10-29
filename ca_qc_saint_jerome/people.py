from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.vsj.ca/conseil-municipal-et-comite-executif/membres-du-conseil-municipal"


class SaintJeromePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE, encoding="utf-8")
        councillors = page.xpath('//div[contains(@class," inner_member")]')
        assert len(councillors), "No councillors found"

        for councillor in councillors:
            name = councillor.xpath(".//h2/text()")[0]
            district = councillor.xpath('.//div[contains(@class,"district")]/text()')[0].replace("numéro ", "")

            if "Maire" in district:
                district = "Saint-Jérôme"
                role = "Maire"
            else:
                role = "Conseiller"

            image = councillor.xpath('.//div[@class="portrait_single"]/img/@data-lazy-src')[0]
            phone = self.get_phone(councillor, error=False)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.image = image

            if phone:
                p.add_contact("voice", phone, "legislature")
            p.add_contact("email", self.get_email(councillor))

            yield p
