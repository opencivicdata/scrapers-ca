from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'


class TorontoPersonScraper(CSVScraper):
    csv_url = 'https://gist.githubusercontent.com/jpmckinney/ad8afd5e584667f0a369/raw/05dedacf690e77d395178c70b9afd2ee9e4e2a2e/test.csv'
    district_name = '{district name} ({district id})'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
    }
