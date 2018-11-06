from utils import CSVScraper


class NiagaraOnTheLakePersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/niagara-on-the-lake-council
    csv_url = 'https://niagaraopendata.ca/dataset/f002eb93-8046-4d12-9352-af273eb3f7e2/resource/c2ece729-dfef-4b31-8ea7-a1bbfa737d48/download/council.csv'
    many_posts_per_area = True
    unique_roles = ('Lord Mayor', 'Regional Councillor')
