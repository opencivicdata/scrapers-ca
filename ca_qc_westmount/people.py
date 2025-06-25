from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://westmount.org/fr/ville/vie-municipale/bureau-du-maire-et-conseil-municipal"


class WestmountPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath(
            '//section[contains(@class, "o-section--rubrics")][1]//div[contains(@class, "c-rubrics__list")]//div[contains(@class, "c-rubric-card ")]'
        )
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath('.//h2[@class="c-rubric-card__title"]')[0].text_content()
            district = councillor.xpath('.//span[@class="c-rubric-card__surtitle"]')[0].text_content()
            if "Maire" in district:
                role = "Maire"  # To replace Mairesse
                district = "Westmount"
            else:
                role = "Conseiller"

            email = self.get_email(councillor, error=False)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            p.image = councillor.xpath(".//img/@src")[0]
            if email:
                p.add_contact("email", email)

            yield p
