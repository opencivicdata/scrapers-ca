from utils import CSVScraper


class TorontoPersonScraper(CSVScraper):
    # https://open.toronto.ca/dataset/elected-officials-contact-information/
    csv_url = "https://ckan0.cf.opendata.inter.prod-toronto.ca/dataset/27aa4651-4548-4e57-bf00-53a346931251/resource/dea217a2-f7c1-4e62-aec1-48fffaad1170/download/2022-2026%20Elected%20Officials%20Contact%20Info.csv"
    corrections = {
        "district name": {
            "Scarborough East": "Scarborough-Guildwood",
        },
        "email": {
            "councillor_ mckelvie@toronto.ca": "councillor_mckelvie@toronto.ca",
        },
    }

    def is_valid_row(self, row):
        return row["first name"] != "None" and row["last name"] != "None"
