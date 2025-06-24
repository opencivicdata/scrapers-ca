from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.dorval.qc.ca/en/the-city/democratic-life/municipal-council"


class DorvalPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="c-rubric-card || js-accordion"]')[:-3]
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//h2[@class="c-rubric-card__title"]')[0].text_content()
            info = councillor.xpath('.//span[@class="c-rubric-card__surtitle"]')[0].text_content()
            if "Vacant" not in info:
                if "Mayor" in info:
                    district = "Dorval"
                    role = "Maire"
                else:
                    district = info.split(" – ")[1]
                    role = "Conseiller"
                p = Person(primary_org="legislature", name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)

                p.image = councillor.xpath('.//img[contains(@class, "c-rubric-card__img")]/@src')[0]

                email = self.get_email(councillor)
                p.add_contact("email", email)

                yield p
