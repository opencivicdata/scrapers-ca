import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2fconseil_municipal"
MAYOR_CONTACT_PAGE = "http://www.gatineau.ca/portail/default.aspx?p=la_ville/conseil_municipal/maire"


class GatineauPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # it's all javascript rendered on the client... wow.
        js = page.xpath('string(//div[@id="contenu-principal-centre-contenu-index"]/script[2])')  # allow string()
        districts = re.findall(r'arrayDistricts\[a.+"(.+)"', js)
        names = re.findall(r'arrayMembres\[a.+"(.+)"', js)
        urls = re.findall(r'arrayLiens\[a.+"(.+)"', js)
        # first item in list is mayor
        p = Person(primary_org="legislature", name=names[0], district="Gatineau", role="Maire")
        p.add_source(COUNCIL_PAGE)
        p.add_source(MAYOR_CONTACT_PAGE)
        email = "maire@gatineau.ca"  # hardcoded
        p.add_contact("email", email)
        yield p

        councillors = list(zip(districts, names, urls))[1:]
        assert len(councillors), "No councillors found"
        for raw_district, name, url in councillors:
            if name == "Vacant":
                continue

            profile_url = COUNCIL_PAGE + "/" + url.split("/")[-1]
            profile_page = self.lxmlize(profile_url)
            photo_url = profile_page.xpath('//div[@class="colonnes-2"]//img/@src')[0]
            district = "District " + re.search(r"\d+", raw_district).group(0)
            email = self.get_email(profile_page)
            p = Person(primary_org="legislature", name=name, district=district, role="Conseiller")
            p.add_source(COUNCIL_PAGE)
            p.add_source(profile_url)
            p.image = photo_url
            p.add_contact("email", email)
            yield p
