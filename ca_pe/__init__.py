# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class PrinceEdwardIsland(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:pe/legislature'
  geographic_code = 11
  division_name = 'Prince Edward Island'
  name = 'Legislative Assembly of Prince Edward Island'
  url = 'http://www.assembly.pe.ca'
  parties = [
    {'name': 'Liberal Party of Prince Edward Island'},
    {'name': 'Progressive Conservative Party of Prince Edward Island'},
  ]
