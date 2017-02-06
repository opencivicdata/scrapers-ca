from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class King(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519049'
    division_name = 'King'
    name = 'King Township Council'
    url = 'http://www.king.ca'
