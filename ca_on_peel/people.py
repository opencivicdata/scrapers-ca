from utils import CSVScraper


class PeelPersonScraper(CSVScraper):
    # https://data.peelregion.ca/datasets/RegionofPeel::peel-ward-boundary/explore?layer=1
    csv_url = "https://services6.arcgis.com/ONZht79c8QWuX759/arcgis/rest/services/Peel_Ward_Boundary/FeatureServer/replicafilescache/Peel_Ward_Boundary_-3456469171846657907.csv"
    many_posts_per_area = True
