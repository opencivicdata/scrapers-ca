from utils import CSVScraper


class NiagaraOnTheLakePersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/niagara-on-the-lake-council
    csv_url = "https://niagaraopendata.ca/dataset/f002eb93-8046-4d12-9352-af273eb3f7e2/resource/8f5d0dd9-1721-45d9-956c-807463cbecc0/download/council2019.csv"
    many_posts_per_area = True
    unique_roles = ("Lord Mayor", "Regional Councillor")
