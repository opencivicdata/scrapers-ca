from utils import CSVScraper

from datetime import date


class TorontoCandidatesPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSBiU-M3w3hlEsdcnN_F6mYlYf5PmvsSpN73V3rbUVYK4JpI99acfZewhQ9EmZtG4niQRdy8EFDR53a/pub?gid=1564068820&single=true&output=csv'
    updated_at = date(2018, 9, 19)
    contact_person = 'andrew@newmode.net'
    encoding = 'utf-8'
    corrections = {
        'district name': {
            'Humber River-Black Creek': 'Humber River—Black Creek',
            'Scarborough-Agincourt': 'Scarborough—Agincourt',
            'Eglinton-Lawrence': 'Eglinton—Lawrence',
            'Spadina-Fort York': 'Spadina—Fort York',
            'Beaches-East York': 'Beaches—East York',
            'Scarborough-Rouge Park': 'Scarborough—Rouge Park',
            'York South-Weston': 'York South—Weston',
            'Parkdale-High Park': 'Parkdale—High Park',
            'Scarborough-Guildwood': 'Scarborough—Guildwood',
            'Etobicoke-Lakeshore': 'Etobicoke—Lakeshore',
            'Toronto-St. Paul\'s': 'Toronto—St. Paul\'s',
            'University-Rosedale': 'University—Rosedale',
            'Toronto-Danforth': 'Toronto—Danforth',
        },
    }

    def is_valid_row(self, row):
        return any(row.values()) and row['last name'] and row['first name']
