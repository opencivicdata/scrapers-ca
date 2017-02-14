from utils import CSVScraper


class LangleyPersonScraper(CSVScraper):
    csv_url = 'https://data.tol.ca/api/views/ykn8-vbpf/rows.csv?accessType=DOWNLOAD'
    many_posts_per_area = True
