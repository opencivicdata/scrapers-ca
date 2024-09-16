import json

import lxml.html
from django.template.defaultfilters import slugify

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
            return lxml.html.fromstring(content)

        page = get_content(COUNCIL_PAGE)
        councillors = page.xpath("//a[.//h3]")
        assert len(councillors), "No councillors found"
        for councillor in councillors:
            districts = []
            name = councillor.xpath(".//h3")[0].text_content()
            role = councillor.xpath('.//div[@class="poste"]')[0].text_content()

            if "Maire" in role:
                role = "Maire"
                district = "Sherbrooke"
            else:
                role = "Conseiller"
                district = councillor.xpath('.//div[@class="district"]')[0].text_content()
                district = clean_french_prepositions(district).replace("District", "").strip()
                if district == "Lac-Magog":
                    district = "Lac Magog"

            districts.append(district)

            if "président" in role:
                borough = councillor.xpath('.//div[@class="bloc_bas"]/p')[0].text_content()
                borough = clean_french_prepositions(borough).replace("Arrondissement", "").strip()

                if borough == "Brompton-Rock Forest-Saint-\u00c9lie-Deauville":
                    borough = "Brompton–Rock Forest–Saint-Élie–Deauville"  # N-dashes
                if borough != district:  # Lennoxville
                    districts.append(borough)

            url = "https://www.sherbrooke.ca" + councillor.xpath("./@href")[0]
            page = get_content(url)

            phone = self.get_phone(page, error=False)
            email = self.get_email(page, error=False)
            image = councillor.xpath(".//@src")[0]
            if "https://" not in image:
                image = "https://contenu.maruche.ca" + image

            for i, district in enumerate(districts):
                p = Person(primary_org="legislature", name=name, district=district, role=role)
                p.add_source(COUNCIL_PAGE)
                p.add_source(url)
                p.image = image

                if email:
                    p.add_contact("email", email)
                if phone:
                    p.add_contact("voice", phone, "legislature")
                if i:
                    p._related[0].extras["boundary_url"] = f"/boundaries/sherbrooke-boroughs/{slugify(district)}/"
                yield p
