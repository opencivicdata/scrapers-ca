# coding: utf-8
from utils import CanadianJurisdiction


class Alberta(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:ab/legislature'
  geographic_code = 48
  division_name = u'Alberta'
  name = u'Legislative Assembly of Alberta'
  url = 'https://www.assembly.ab.ca'
  parties = [
    {'name': 'Alberta Liberal Party'},
    {'name': 'Alberta New Democratic Party'},
    {'name': 'Progressive Conservative Association of Alberta'},
    {'name': 'Wildrose Alliance Party'},
    {'name': 'Independent'},
  ]
