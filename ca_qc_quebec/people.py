import re

from django.template.defaultfilters import slugify

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://www.ville.quebec.qc.ca/apropos/gouvernance/conseil-municipal/membres.aspx"


class QuebecPersonScraper(CanadianScraper):
    def scrape(self):
        page = self.lxmlize(COUNCIL_PAGE)

        sections = page.xpath('//div[contains(@class, "membres-conseil-municipal")]')
        for section in sections:
            councillors = section.xpath("./div")
            assert len(councillors), "No councillors found"
            for councillor in councillors:
                name = " ".join(reversed(councillor.xpath("./h3//text()")))
                if "vacant" in name.lower():
                    continue

                header = section.xpath("./preceding-sibling::h2/text()")[-1]
                if "Mairie" in header:
                    district = "Québec"
                    role = "Maire"
                else:
                    district = councillor.xpath('./p[@itemprop="jobTitle"]/a/text()')[0]
                    district = (
                        re.search(r"\ADistrict (?:de(?: la)?|du|des) ([\w —–-]+)", district, flags=re.UNICODE)
                        .group(1)
                        .strip()
                    )
                    role = "Conseiller"

                if district == "Saules–Les Méandres":
                    district = "Les Saules"
                elif district == "Neufch\u00e2tel\u2013Lebourgneuf":
                    district = "Neufchâtel-Lebourgneuf"
                elif district == "Loretteville\u2013Les Ch\u00e2tels":
                    district = "Loretteville-Les Ch\u00e2tels"
                else:
                    district = re.sub(r"–", "—", district)  # n-dash, m-dash

                districts = [district]

                borough = None
                borough_strings = councillor.xpath('.//p[@itemprop = "affiliation"]/text()')
                for string in borough_strings:
                    borough = re.findall(r"Présidente? de l’arrondissement (.*)$", string)
                    if borough:
                        borough = borough[0].replace("des", "Les").replace("de ", "")
                        districts.append(borough)

                for i, district in enumerate(districts):
                    p = Person(primary_org="legislature", name=name, district=district, role=role)
                    p.add_source(COUNCIL_PAGE)
                    p.image = councillor.xpath("./figure//@src")[0]
                    p.add_contact("voice", self.get_phone(councillor, area_codes=[418]), "legislature")
                    if i:
                        p._related[0].extras["boundary_url"] = f"/boundaries/quebec-boroughs/{slugify(district)}/"
                    yield p
