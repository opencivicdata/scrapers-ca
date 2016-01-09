from __future__ import unicode_literals
from utils import CSVScraper

COUNCIL_PAGE = 'http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=c3a83293dc3ef310VgnVCM10000071d60f89RCRD'


class TorontoPersonScraper(CSVScraper):
    csv_url = 'http://www1.toronto.ca/City%20Of%20Toronto/Information%20&%20Technology/Open%20Data/Data%20Sets/Assets/Files/Toronto_Elected_Officials.csv'
    district_id_to_district_name = '{}'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
    }

    # TODO: Remove once original file is fixed.
    # See: https://github.com/opencivicdata/scrapers-ca/issues/155#issuecomment-169855328
    csv_url = 'https://gist.githubusercontent.com/patcon/70656c30f544efd3673a/raw/4fc61631243da8dea0a4f4b31f5d5a5b99f26c75/Toronto_Elected_Officials.csv'
