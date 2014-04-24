# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class Canada(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/legislature'
  geographic_code = 1
  division_name = 'Canada'
  name = 'Parliament of Canada'
  url = 'http://www.parl.gc.ca'
  chambers = {
    'lower': {
      'name': 'House of Commons',
      'title': 'MP',
    },
    'upper': {
      'name': 'Senate',
      'title': 'Senator',
    },
  }
  parties = [
    {'name': 'Bloc Québécois'},
    {'name': 'Conservative'},
    {'name': 'Conservative Independent'},
    {'name': 'Green Party'},
    {'name': 'Independent'},
    {'name': 'Liberal'},
    {'name': 'NDP'},
  ]
