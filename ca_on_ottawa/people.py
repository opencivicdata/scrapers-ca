from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    # https://open.ottawa.ca/documents/ottawa::elected-officials-2022-2026/about
    csv_url = "https://www.arcgis.com/sharing/rest/content/items/a5e9dc2425274bb796d3ded47b0d7b00/data"
    fallbacks = {"district name": "ward name"}
    extension = ".xls"
