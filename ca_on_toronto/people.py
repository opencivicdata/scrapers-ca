from utils import CSVScraper


class TorontoPersonScraper(CSVScraper):
    # https://www.toronto.ca/city-government/data-research-maps/open-data/open-data-catalogue/#3bdfa14a-7792-04e7-6c8a-c33b6395b5e4
    csv_url = 'https://www.toronto.ca/ext/open_data/catalog/data_set_files/Councillor_Contact_Data_December_2018.xlsx'
    encoding = 'windows-1252'
    other_names = {
        'Norman Kelly': ['Norm Kelly'],
        'Justin Di Ciano': ['Justin J. Di Ciano'],
        'John Filion': ['John Fillion'],
        'Michelle Berardinetti': ['Michelle Holland'],
    }
    corrections = {
        'district name': {
            'Scarborough East ': 'Scarborough-Guildwood',
        },
        'email': {
            'councillor_ mckelvie@toronto.ca ': 'councillor_mckelvie@toronto.ca',
        },
    }
