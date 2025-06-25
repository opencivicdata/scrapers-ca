from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = (
    "https://www.pointe-claire.ca/democratie-et-participation-citoyenne/conseil-municipal/votre-conseil-municipal"
)


class PointeClairePersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        councillors = page.xpath('//div[@class="listing-council-members"]//div[contains(@class, "single-member")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = " ".join([n.strip() for n in councillor.xpath(".//h2/text()")])
            district = councillor.xpath('.//div[@class="member-location"]')[0].text_content().strip()
            if district == "Pointe-Claire":
                role = "Maire"
            else:
                role = "Conseiller"
                district = district.split(" - ")[0].strip()

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.image = councillor.xpath('.//div[@class="member-photo"]/img/@src')[0]
            p.add_contact("email", self.get_email(councillor))
            p.add_contact("voice", self.get_phone(councillor, area_codes=[514]), "legislature")
            p.add_source(COUNCIL_PAGE)
            yield p
