from __future__ import unicode_literals
from utils import CSVScraper


class NiagaraPersonScraper(CSVScraper):
    # The new data file:
    # * has underscores in headers
    # * uses "District_ID" instead of "District name"
    # * prefixes "District_ID" with "Niagara Region - "
    # https://www.niagaraopendata.ca//dataset/ee767222-c7fc-4541-8cad-a27276a3522b/resource/af5621ad-c2e4-4569-803f-4aadca4173be/download/councilelectedofficials.csv
    csv_url = 'http://www.niagararegion.ca/test/sherpa-list-to-csv.aspx?list=council-elected-officials-csv'
    many_posts_per_area = True
