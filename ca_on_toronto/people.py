from utils import CSVScraper


class TorontoPersonScraper(CSVScraper):
    csv_url = 'https://www.toronto.ca/ext/open_data/catalog/data_set_files/Councillor%20Contact%20Data%20November%202%202017.xlsx'
    district_name_format_string = '{district name} ({district id})'
    encoding = 'windows-1252'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
        'John Filion': ['John Fillion'],
        'Michelle Berardinetti': ['Michelle Holland'],
    }
