import json

import lxml.html

from utils import CanadianPerson as Person
from utils import CanadianScraper, clean_french_prepositions

COUNCIL_PAGE = "https://www.sherbrooke.ca/fr/vie-municipale/elues-et-elus-municipaux"


class SherbrookePersonScraper(CanadianScraper):
    def scrape(self):
        districts = []

        # The whole site is rendered with Javascript, but has part of the html documents in the scripts
        def get_content(url):
            page = self.lxmlize(url)
            script = page.xpath(".//script[not(@type)]")[0].text_content()
            data = script.split(" = ", 1)[1]
            data = json.loads(data)
            content = data["value"]["selected"]["content"]["fr"]
            page = lxml.html.fromstring(content)
            return page

        page = get_content(COUNCIL_PAGE)
        councillors = page.xpath("//a[.//h3]")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            name = councillor.xpath(".//h3")[0].text_content()
            role = councillor.xpath('.//div[@class="poste"]')[0].text_content()

            if "Maire" in role:
                role = "Maire"
                district = "Sherbrooke"
            else:
                role = "Conseiller"
                district = councillor.xpath('.//div[@class="district"]')[0].text_content()
                district = clean_french_prepositions(district).replace("District", "").strip()

            if district == "Lennoxville":
                district = "Arrondissement 3"
            elif district == "Lac-Magog":
                district = "Lac Magog"
            districts.append(district)
            url = "https://www.sherbrooke.ca" + councillor.xpath("./@href")[0]
            page = get_content(url)

            p = Person(primary_org="legislature", name=name, district=district, role=role)
            p.add_source(COUNCIL_PAGE)
            p.add_source(url)
            image = councillor.xpath(".//@src")[0]
            if "https://" not in image:
                image = "https://contenu.maruche.ca" + image
            p.image = image
            phone = self.get_phone(page, error=False)
            email = self.get_email(page, error=False)
            if email:
                p.add_contact("email", email)
            if phone:
                p.add_contact("voice", phone, "legislature")
            if district == "Brompton":
                p._related[0].extras["boundary_url"] = "/boundaries/sherbrooke-boroughs/brompton/"
            elif district == "Arrondissement 3":
                p._related[0].extras["boundary_url"] = "/boundaries/sherbrooke-boroughs/lennoxville/"
            yield p
