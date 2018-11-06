from utils import CSVScraper


class GrimsbyPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/town-of-grimsby-elected-officials
    csv_url = 'https://niagaraopendata.ca/dataset/fe096749-6ca8-4ae7-b80e-dc682a698759/resource/892a4873-cbe7-4c32-9b70-9f364467955e/download/grimsbycouncil20160210.csv'
    many_posts_per_area = True
