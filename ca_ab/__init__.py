# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class Alberta(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:ab/legislature'
  geographic_code = 48
  division_name = 'Alberta'
  name = 'Legislative Assembly of Alberta'
  url = 'https://www.assembly.ab.ca'
  parties = [
    {'name': 'Alberta Liberal Party'},
    {'name': 'Alberta New Democratic Party'},
    {'name': 'Progressive Conservative Association of Alberta'},
    {'name': 'Wildrose Alliance Party'},
    {'name': 'Independent'},
  ]
