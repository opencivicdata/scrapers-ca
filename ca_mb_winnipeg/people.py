import json

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "https://winnipeg.ca/council/"


class WinnipegPersonScraper(CanadianScraper):
    def scrape(self):
        # from https://data.winnipeg.ca/Council-Services/Council-Data/r4tk-7dip/about_data
        api_url = "https://data.winnipeg.ca/resource/r4tk-7dip.json"
        data = json.loads(self.get(api_url).content)
        assert len(data), "No councillors found via API"

        for item in data:
            if not item["current_council"]:
                continue
            name = item["person"]
            if name == "Vacant":
                continue
            role = item["position_english"]
            district = item["name_english"].replace(" - ", "—")
            phone = item.get("phone", "")
            fax = item.get("fax", "")

            p = Person(primary_org="legislature", name=name, role=role, district=district)

            if phone:
                p.add_contact("voice", phone, "legislature")
            if fax:
                p.add_contact("fax", fax, "legislature")
            p.add_source(api_url)
            if "portrait" in item:
                p.image = item["portrait"]
            yield p
