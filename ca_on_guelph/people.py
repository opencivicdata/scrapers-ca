from utils import CSVScraper


class GuelphPersonScraper(CSVScraper):
    # https://explore.guelph.ca/documents/5ec8d85028c94e83be12a9f01d14eb7f/about
    csv_url = "https://gismaps.guelph.ca/OpenData/guelph-city-council.csv"
    many_posts_per_area = True
