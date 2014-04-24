# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class NewfoundlandAndLabrador(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:nl/legislature'
  geographic_code = 10
  division_name = 'Newfoundland and Labrador'
  name = 'Newfoundland and Labrador House of Assembly'
  url = 'http://www.assembly.nl.ca'
  parties = [
    {'name': 'Progressive Conservative Party of Newfoundland and Labrador'},
    {'name': 'New Democratic Party of Newfoundland and Labrador'},
    {'name': 'Liberal Party of Newfoundland and Labrador'},
  ]
