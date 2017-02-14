from utils import CSVScraper

from datetime import date


class GeorginaPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1wf91UJK7dluBFHV3v7ubINzL4lCxnoaFqRcYHdFv9oo/pub?gid=1034669665&single=true&output=csv'
    many_posts_per_area = True
    unique_roles = ('Mayor', 'Regional Councillor')
    created_at = date(2016, 11, 8)
    contact_person = 'andrew@newmode.net, shamus@newmode.net'
