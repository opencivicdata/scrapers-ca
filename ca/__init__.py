# coding: utf-8
from utils import CanadianJurisdiction


class Canada(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/legislature'
  geographic_code = 01
  division_name = u'Canada'
  name = u'Parliament of Canada'
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
    {'name': u'Bloc Québécois'},
    {'name': u'Conservative'},
    {'name': u'Conservative Independent'},
    {'name': u'Green Party'},
    {'name': u'Independent'},
    {'name': u'Liberal'},
    {'name': u'NDP'},
  ]
