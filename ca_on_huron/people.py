import json

from utils import CSVScraper


class HuronPersonScraper(CSVScraper):
    # https://data-huron.opendata.arcgis.com/datasets/051e72a02edc4337af8ca2606ab58644_0
    csv_url = "https://opendata.arcgis.com/datasets/051e72a02edc4337af8ca2606ab58644_0.csv"
    encoding = "utf-8-sig"
    many_posts_per_area = True
    corrections = {
        "primary role": {
            "Councilor": "Councillor",
        },
        "phone": lambda value: value.replace(", ", ";"),
    }

    # removing the seat number added to districts with just 1 Councillor
    def scrape(self):
        single_councillor_districts = ["Howick", "Morris-Turnberry", "North Huron"]
        people = super().scrape()
        for p in people:
            data = p._related[0].post_id.replace("~", "")
            membership = json.loads(data)
            for district in single_councillor_districts:
                if membership["label"] == "{} (seat 1)".format(district):
                    membership["label"] = district
                    p._related[0].post_id = "~" + json.dumps(membership)
            yield p
