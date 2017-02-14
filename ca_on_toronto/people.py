from __future__ import unicode_literals
from utils import CSVScraper


class TorontoPersonScraper(CSVScraper):
    csv_url = 'http://www1.toronto.ca/City%20Of%20Toronto/Information%20&%20Technology/Open%20Data/Data%20Sets/Assets/Files/Toronto_Elected_Officials.csv'
    district_name_format_string = '{district name} ({district id})'
    encoding = 'windows-1252'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
        'John Filion': ['John Fillion'],
        'Michelle Berardinetti': ['Michelle Holland'],
    }
