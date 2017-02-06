from __future__ import unicode_literals
from utils import CSVScraper

from datetime import date


class KingPersonScraper(CSVScraper):
    csv_url = 'https://docs.google.com/spreadsheets/d/1wf91UJK7dluBFHV3v7ubINzL4lCxnoaFqRcYHdFv9oo/pub?gid=1105544164&single=true&output=csv'
    created_at = date(2016, 11, 8)
    contact_person = 'andrew@newmode.net, shamus@newmode.net'
