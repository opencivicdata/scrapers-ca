from utils import CSVScraper


class StrathconaCountyPersonScraper(CSVScraper):
    # https://opendata.arcgis.com/api/v3/datasets/b7b1aa0fbad6445c8aa8ab66cb13347f_0/downloads/data?format=csv&spatialRefId=3857&where=1%3D1
    csv_url = (
        "https://opendata-strathconacounty.hub.arcgis.com/datasets/StrathconaCounty::county-council-2021-2025/about"
    )
    corrections = {
        "district name": {
            "Strathcona": "Strathcona County",
        }
    }

    def header_converter(self, s):
        s = super().header_converter(s)
        if s == "district id":
            return "district name"
        return s
