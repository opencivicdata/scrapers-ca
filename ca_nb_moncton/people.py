import json
from collections import defaultdict

from utils import CanadianPerson as Person
from utils import CanadianScraper

# from https://open.moncton.ca/datasets/elected-officials/explore
API_URL = "https://services1.arcgis.com/E26PuSoie2Y7bbyI/arcgis/rest/services/Elected_Officials/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"


class MonctonPersonScraper(CanadianScraper):
    def scrape(self):
        seat_numbers = defaultdict(int)
        data = json.loads(self.get(API_URL).content)["features"]
        assert len(data), "No councillors found"

        for item in data:
            councillor = item["properties"]
            ward = councillor["WardName"]
            if ward != "Moncton":
                ward = "Ward " + ward
            role = councillor["Primary_role"]
            if role != "Mayor":
                seat_numbers[ward] += 1
                district = ward + f" (seat {seat_numbers[ward]})"
            else:
                district = ward
            name = councillor["Name"]
            email = councillor["Email"]
            phone = councillor["Phone"]
            fax = councillor["Fax"]

            p = Person(primary_org="legislature", name=name, district=district, role=role)

            if phone:
                p.add_contact("voice", p.clean_telephone_number(phone), "legislature")
            if fax:
                p.add_contact("fax", p.clean_telephone_number(fax), "legislature")
            if email:
                p.add_contact("email", email)

            p.image = councillor["Photo_URL"]
            p.add_source(API_URL)

            yield p
