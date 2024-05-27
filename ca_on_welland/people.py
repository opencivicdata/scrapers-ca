from utils import CSVScraper


class WellandPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/city-of-welland-mayor-and-council-members
    csv_url = "https://opendata.arcgis.com/api/v3/datasets/e4f572b37d934bce9e73ca16a4a2e48d_1/downloads/data?format=csv&spatialRefId=4326&where=1%3D1"
    encoding = "windows-1252"
    many_posts_per_area = True
