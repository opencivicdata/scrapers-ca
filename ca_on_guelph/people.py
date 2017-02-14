from utils import CSVScraper


class GuelphPersonScraper(CSVScraper):
    csv_url = 'http://open.guelph.ca/wp-content/uploads/2015/01/GuelphCityCouncil2014-2018ElectedOfficalsContactInformation1.csv'
    many_posts_per_area = True
