# coding: utf-8
from __future__ import unicode_literals
from utils import CanadianJurisdiction


class BritishColumbia(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:bc'
    division_name = 'British Columbia'
    name = 'Legislative Assembly of British Columbia'
    url = 'http://www.leg.bc.ca'
    parties = [
        {'name': 'New Democratic Party of British Columbia'},
        {'name': 'British Columbia Liberal Party'},
    ]
