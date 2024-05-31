from django.template.defaultfilters import slugify

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.levis.qc.ca/la-ville/conseil-municipal/elus/"
ARRONDISSEMENTS_PAGE = "https://www.ville.levis.qc.ca/la-ville/arrondissements/conseils/"


class LevisPersonScraper(CanadianScraper):
    def scrape(self):
        council_page = self.lxmlize(COUNCIL_PAGE)
        arrondissements_page = self.lxmlize(ARRONDISSEMENTS_PAGE)

        presidents = {}
        for president in arrondissements_page.xpath('//p[contains(./b, "Président")]'):
            arrondissement = (
                president.xpath('./ancestor::div[@class="drawer"]//a')[0]
                .text_content()
                .replace("Arrondissement ", "")
                .replace("des", "Les")
                .replace("de ", "")
            )
            name = president.xpath("./text()")[0].strip().replace("\xa0", " ")
            presidents[name] = arrondissement

        councillors = council_page.xpath('//div[@class="drawers"]//div[@class="dropdown"]')
        assert len(councillors), "No councillors found"
        for person in councillors:
            position, name = person.xpath("./h3/text()")[0].replace("–", "-").split(" - ")
            if "," in position:
                role, district = position.title().split(", ")[0].split(" ", 1)
            else:
                role = "Maire"
                district = "Lévis"

            if role == "Conseillère":
                role = "Conseiller"

            photo_url = person.xpath(".//img/@src")[0]
            email = self.get_email(person)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)

            if name in presidents:
                p.add_source(ARRONDISSEMENTS_PAGE)  # making sure the sources match for both memberships

                person = Person(primary_org="legislature", name=name, district=presidents[name], role="Président")
                person.add_source(COUNCIL_PAGE)
                person.add_source(ARRONDISSEMENTS_PAGE)

                person.image = photo_url
                person.add_contact("email", email)
                person._related[0].extras["boundary_url"] = f"/boundaries/levis-boroughs/{slugify(presidents[name])}/"

                yield person

            p.image = photo_url
            p.add_contact("email", email)

            yield p
