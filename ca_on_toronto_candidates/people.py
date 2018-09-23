from utils import CSVScraper

from datetime import date


class TorontoCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSBiU-M3w3hlEsdcnN_F6mYlYf5PmvsSpN73V3rbUVYK4JpI99acfZewhQ9EmZtG4niQRdy8EFDR53a/pub?gid=1564068820&single=true&output=csv'
    updated_at = date(2018, 9, 19)
    contact_person = 'andrew@newmode.net'
    encoding = 'utf-8'
    corrections = {
        # Correct hyphen to m-dash.
        'district name': {
            '': 'Toronto',
            'Beaches-East York': 'Beaches—East York',
            'Eglinton-Lawrence': 'Eglinton—Lawrence',
            'Etobicoke-Lakeshore': 'Etobicoke—Lakeshore',
            'Humber River-Black Creek': 'Humber River—Black Creek',
            'Parkdale-High Park': 'Parkdale—High Park',
            'Scarborough-Agincourt': 'Scarborough—Agincourt',
            'Scarborough-Guildwood': 'Scarborough—Guildwood',
            'Scarborough-Rouge Park': 'Scarborough—Rouge Park',
            'Spadina-Fort York': 'Spadina—Fort York',
            'Toronto-Danforth': 'Toronto—Danforth',
            'Toronto-St. Paul\'s': 'Toronto—St. Paul\'s',
            'University-Rosedale': 'University—Rosedale',
            'York South-Weston': 'York South—Weston',
        },
    }
