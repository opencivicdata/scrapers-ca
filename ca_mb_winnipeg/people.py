import json
import re

import requests

from utils import CanadianPerson as Person
from utils import CanadianScraper

COUNCIL_PAGE = "http://winnipeg.ca/council/"


class WinnipegPersonScraper(CanadianScraper):
    def scrape(self):
        # https://winnipeg.ca/council/wards/includes/wards.js
        # var COUNCIL_API = 'https://data.winnipeg.ca/resource/r4tk-7dip.json';
        api_url = "https://data.winnipeg.ca/resource/r4tk-7dip.json"
        data = json.loads(requests.get(api_url).content)

        page = self.lxmlize(COUNCIL_PAGE)
        councillors = page.xpath('//div[@class="card link h-100"]')
        for item in data:
            if not item["current_council"]:
                continue
            name = item["person"]
            role = item["position_english"]
            district = item["name_english"].replace(" - ","—")
            email = item["email_link_english"]
            if "phone" in item:
                phone = item["phone"]
            fax = item["fax"]
            
            p = Person(primary_org="legislature",name=name, role=role, district=district)
            if "@" in email:
                p.add_contact("email",email)
            p.add_contact("voice",phone,"legislature")
            p.add_contact("fax",fax,"legislature")
            p.add_source(api_url)
            p.add_source(COUNCIL_PAGE)
            for councillor in councillors:
                if name == councillor.xpath('.//a[@class="full-card-link"]')[0].text_content(): # matching names
                    p.image = councillor.xpath('.//img/@src')[0]
            yield p

#         page = self.lxmlize(COUNCIL_PAGE, "utf-8")

#         councillors = page.xpath('//div[@class="box"]')
#         assert len(councillors), "No councillors found"
#         for councillor in councillors:
#             role = councillor.xpath('.//div[@class="insideboxtitle"]/text()')[0].strip()
#             name = councillor.xpath('.//p[@class="insideboxtext"]/text()')[0]
#             image = councillor.xpath(".//@src")[0]

#             if "Councillor" in name:
#                 role = "Councillor"
#                 name = name.replace("Councillor ", "")

#             url = api_url
#             item = next((item for item in data if item["person"] == name and item["current_council"]), None)
#             if item is None:
#                 raise Exception(name)

#             district = item["name_english"].replace(" - ", "—")  # hyphen, m-dash

#             email = item["email_link"]
#             voice = item["phone"]
#             fax = item["fax"]

#             p = Person(primary_org="legislature", name=name, district=district, role=role)
#             p.add_source(COUNCIL_PAGE)
#             p.add_source(url)

#             if not image.endswith("nophoto.jpg"):
#                 p.image = image
#             p.add_contact("email", parse_email(email))
#             p.add_contact("voice", voice, "legislature")
#             p.add_contact("fax", fax, "legislature")

#             yield p


# def parse_email(email):
#     return re.search("=([^&]+)", email).group(1) + "@winnipeg.ca"
