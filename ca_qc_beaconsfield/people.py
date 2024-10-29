from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.beaconsfield.ca/fr/notre-ville/conseil-de-ville-et-districts-electoraux"


class BeaconsfieldPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[contains(@class, "c-rubric-card__header")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h2")[0].text_content().strip()
            district = councillor.xpath(".//span")[0].text_content().strip()
            if district == "Maire":
                district = "Beaconsfield"
                role = "Maire"
            else:
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath(".//@src")[0]
            p.add_contact("email", self.get_email(councillor, "./following-sibling::div"))
            p.add_source(COUNCIL_PAGE)
            yield p
