import csv
from io import StringIO

from utils import CanadianPerson as Person
from utils import CanadianScraper

CSV_URL = "http://opendata-city-of-waterloo.opendata.arcgis.com/datasets/594698f0bbcd4c20b72977194d2b97b8_0.csv"


class WaterlooPersonScraper(CanadianScraper):
    def scrape(self):
        response = self.get(CSV_URL)
        rows = csv.DictReader(StringIO(response.text))
        people = 0

        for row in rows:
            name = row.get("NAME", "").strip()
            if not name or name == "Vacant":
                continue

            role = row.get("PRIMARY_ROLE", "").strip()
            district = row.get("DISTRICT_NAME", "").strip() or "Waterloo"
            image = row.get("PHOTO_URL", "").strip() or None

            p = Person(primary_org="legislature", name=name, district=district, role=role, image=image)
            p.add_source(row.get("SOURCE_URL", "").strip() or CSV_URL)

            email = row.get("EMAIL", "").strip()
            if email:
                p.add_contact("email", email)

            phone = row.get("PHONE", "").strip()
            if phone:
                p.add_contact("voice", phone, "legislature")

            for key in ("WEBSITE", "FACEBOOK", "INSTAGRAM", "TWITTER", "LINKEDIN", "YOUTUBE"):
                link = row.get(key, "").strip()
                if link:
                    p.add_link(link)

            people += 1
            yield p

        assert people, "No councillors found"
