from utils import CSVScraper


class VancouverPersonScraper(CSVScraper):
    # https://data.vancouver.ca/datacatalogue/councilContactInfo.htm
    csv_url = 'ftp://webftp.vancouver.ca/OpenData/csv/ElectedOfficialsContactInformation.csv'
    many_posts_per_area = True
    corrections = {
        'fax': {
            'N/A': None,
        },
    }
