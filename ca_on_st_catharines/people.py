import re

from utils import CSVScraper


class StCatharinesPersonScraper(CSVScraper):
    # https://niagaraopendata.ca/dataset/st-catharines-councilors
    csv_url = "https://niagaraopendata.ca/dataset/ccb9c7f1-d3b0-4049-9c08-e4f7b048722c/resource/128a39f0-8234-4708-b69b-9c73f7a55475/download/stcathcounsilors.csv"
    many_posts_per_area = True

    def district_name_format_callback(self, name):
        return re.sub("'S", "'s", name.title())
