import re

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://www.gatineau.ca/portail/default.aspx?p=guichet_municipal%2fconseil_municipal"


class GatineauPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        # it's all javascript rendered on the client... wow.
        js = page.xpath('string(//div[@id="contenu-principal-centre-contenu-index"]/script[1])')  # allow string()
        roles = re.findall(r'arrayMembres\[.+?"(.+?)"', js)
        districts = re.findall(r'arrayMembres\[.+?, "(.*?)"', js)
        names = re.findall(r'arrayMembres\[.+?,.+?, "(.*?)"', js)
        urls = re.findall(r'arrayMembres\[.+"(.*?)",', js)

        councillors = list(zip(roles, districts, names, urls))
        assert len(councillors), "No councillors found"
        for role, raw_district, name, url in councillors:
            if name == "Vacant" or "(de " in role:
                continue
            profile_url = COUNCIL_PAGE + "/" + url.split("/")[-1]
            profile_page = self.lxmlize(profile_url)
            photo_url = profile_page.xpath('//div[@class="colonnes-3"]//img/@src')[0]
            if raw_district:
                district = "District " + re.search(r"\d+", raw_district).group(0)
                role = "Conseiller"
            else:
                district = "Gatineau"
                role = "Maire"
            email = self.get_email(profile_page, error=False)
            phone = self.get_phone(profile_page, error=False)
            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(profile_url)
            p.image = photo_url
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            yield p
