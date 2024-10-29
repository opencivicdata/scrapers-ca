import json

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://winnipeg.ca/council/"


class WinnipegPersonScraper(CanadianScraper):
    def scrape(self):
        # from https://data.winnipeg.ca/Council-Services/Council-Data/r4tk-7dip/about_data
        api_url = "https://data.winnipeg.ca/resource/r4tk-7dip.json"
        data = json.loads(self.get(api_url).content)
        assert len(data), "No councillors found via API"

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@class="card link h-100"]')
        assert len(councillors), "No councillors found on website"

        for item in data:
            if not item["current_council"]:
                continue
            name = item["person"]
            role = item["position_english"]
            district = item["name_english"].replace(" - ", "—")
            if "phone" in item:
                phone = item["phone"]
            fax = item["fax"]

            p = Person(primary_org="legislature", name=name, role=role, district=district)

            p.add_contact("voice", phone, "legislature")
            p.add_contact("fax", fax, "legislature")
            p.add_source(api_url)
            p.add_source(COUNCIL_PAGE)
            for councillor in councillors:
                if name == councillor.xpath('.//a[@class="full-card-link"]')[0].text_content():  # matching names
                    p.image = councillor.xpath(".//img/@src")[0]
            yield p
