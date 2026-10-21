from utils import CSVScraper


class OttawaPersonScraper(CSVScraper):
    # https://open.ottawa.ca/documents/ottawa::elected-officials-2022-2026/about
    csv_url = (
        "https://hub.arcgis.com/api/download/v1/items/d099928f2e344b1b909fcf63e5acf3d1/csv?redirect=true&layers=0"
    )

    def header_converter(self, s):
        header = super().header_converter(s).lstrip("\ufeff").removeprefix("\xef\xbb\xbf")
        if header == "ward name":
            return "district name"
        return header

    corrections = {
        "first name": {
            "StÃ©phanie": "Stéphanie",
        },
        "district name": {
            "OrlÃ©ans East-Cumberland": "Orléans East-Cumberland",
            "OrlÃ©ans West-Innes": "Orléans West-Innes",
            "OrlÃ©ans South-Navan": "Orléans South-Navan",
        },
    }
