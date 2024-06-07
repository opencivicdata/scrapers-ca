from django.template.defaultfilters import slugify

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://ville.saguenay.ca/la-ville-et-vie-democratique/conseils-municipaux-et-darrondissement/membres-des-conseils"
MAYOR_PAGE = "https://ville.saguenay.ca"
CONTACT_PAGE = "https://ville.saguenay.ca/la-ville-et-vie-democratique/cabinet"


class SaguenayPersonScraper(CanadianScraper):
    def scrape(self):
        mayor_page = self.lxmlize(MAYOR_PAGE)
        contact_page = self.lxmlize(CONTACT_PAGE)
        name = mayor_page.xpath('//a[contains(., "maire")]/span/text()')[0]
        p = Person(primary_org="legislature", name=name, district="Saguenay", role="Maire")
        p.add_source(MAYOR_PAGE)
        p.add_source(CONTACT_PAGE)
        node = contact_page.xpath('//h2[contains(., "Coordonnées du cabinet")]/following-sibling::p')[1]
        p.add_contact("voice", self.get_phone(node, area_codes=[418]), "legislature")
        yield p

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[contains(./h3, "District")]')
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            district = councillor.xpath("./h3/text()")[0].replace("#", "")
            name = councillor.xpath(".//p/text()")[0]
            borough = None
            borough_node = councillor.xpath(".//p/strong")
            if borough_node:
                text = borough_node[0].text_content()
                if "Président" in text:
                    borough = text.replace("Président de l'arrondissement de ", "")

            if borough:
                p = Person(primary_org="legislature", name=name, district=borough, role="Conseiller")
                p.add_source(COUNCIL_PAGE)
                p.add_contact("voice", self.get_phone(councillor), "legislature")
                p.add_contact("email", self.get_email(councillor))
                p._related[0].extras["boundary_url"] = f"/boundaries/saguenay-boroughs/{slugify(borough)}/"
                yield p

            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
            p.add_source(COUNCIL_PAGE)
            p.add_contact("voice", self.get_phone(councillor), "legislature")
            p.add_contact("email", self.get_email(councillor))
            yield p
