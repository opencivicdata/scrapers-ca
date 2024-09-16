from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.pointe-claire.ca/fr/membres/"


class PointeClairePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//section[contains(@id, "js-council-member")]')
        assert len(councillors), "No councillors found"
        for index, councillor in enumerate(councillors):
            name = " ".join([n.strip() for n in councillor.xpath(".//h2/text()")])
            district = councillor.xpath(
                './/span[contains(@class, "c-info-list_label")][contains(text(), "District ")]'
            )
            role = "Conseiller"

            if not district and index == 0:
                district = "Pointe-Claire"
                role = "Maire"
            elif district:
                district = district[0].text_content().split(" – ")[0].strip()
            else:
                raise AssertionError("error parsing district")

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath(".//@data-src")[0]
            p.add_contact("email", self.get_email(councillor))
            p.add_contact("voice", self.get_phone(councillor, area_codes=[514]), "legislature")
            p.add_source(COUNCIL_PAGE)
            yield p
