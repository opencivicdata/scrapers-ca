from utils import CSVScraper


class VancouverPersonScraper(CSVScraper):
    # https://data.vancouver.ca/datacatalogue/councilContactInfo.htm
    csv_url = 'https://opendata.vancouver.ca/explore/dataset/elected-officials-contact-information/download/?format=csv&timezone=America/New_York&use_labels_for_header=true&csv_separator=%3B'
    many_posts_per_area = True
    delimiter = ';'
    corrections = {
        'fax': {
            'N/A': None,
        },
    }
