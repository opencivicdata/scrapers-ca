from utils import CSVScraper


class VancouverPersonScraper(CSVScraper):
    csv_url = 'ftp://webftp.vancouver.ca/OpenData/csv/ElectedOfficialsContactInformation.csv'
    many_posts_per_area = True
