from utils import CSVScraper


class SurreyPersonScraper(CSVScraper):
    # 2015-01-22: The CSV is not yet online, so we must manually upload a copy to S3.
    csv_url = 'http://represent.opennorth.ca.s3.amazonaws.com/data/2015-01-22-surrey.csv'
    many_posts_per_area = True
