from __future__ import unicode_literals
from utils import CanadianJurisdiction


class Manitoba(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:mb'
    division_name = 'Manitoba'
    name = 'Legislative Assembly of Manitoba'
    url = 'http://www.gov.mb.ca/legislature/'
    parties = [
        {'name': 'New Democratic Party of Manitoba'},
        {'name': 'Progressive Conservative Party of Manitoba'},
        {'name': 'Manitoba Liberal Party'},
        {'name': 'Independent'},
    ]
