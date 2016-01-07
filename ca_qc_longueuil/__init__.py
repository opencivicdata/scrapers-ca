from __future__ import unicode_literals
from utils import CanadianJurisdiction


class Longueuil(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:2458227'
    division_name = 'Longueuil'
    name = 'Conseil municipal de Longueuil'
    url = 'http://www.longueuil.ca'
    exclude_type_ids = ['district']
