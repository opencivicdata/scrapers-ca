from utils import CSVScraper


class NewWestminsterPersonScraper(CSVScraper):
    # http://opendata.newwestcity.ca/datasets/councillor-contact-information
    csv_url = "http://opendata.newwestcity.ca/downloads/councillor-contact-information/councillor_contacts.csv"
    many_posts_per_area = True
    corrections = {
        "last name": {
            "Cot\x82": "Cote",
        },
    }
