from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://ville.montreal-est.qc.ca/la-ville/conseil-municipal/conseils-municipaux/"


class MontrealEstPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath("//table")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h3")[0].text_content()

            if "maire" in name:
                name = name.split(" ", 2)[-1]
                district = "Montréal-Est"
                role = "Maire"
            else:
                district = "District {}".format(councillor.xpath(".//h3")[1].text_content()[-1])
                role = "Conseiller"

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath(".//@src")[0]
            p.add_contact("email", self.get_email(councillor))
            p.add_source(COUNCIL_PAGE)
            yield p
