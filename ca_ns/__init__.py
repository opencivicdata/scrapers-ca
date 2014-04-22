# coding: utf-8
from utils import CanadianJurisdiction


class NovaScotia(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:ns/legislature'
  geographic_code = 12
  division_name = u'Nova Scotia'
  name = u'Nova Scotia House of Assembly'
  url = 'http://nslegislature.ca/'
  parties = [
      'Liberal',
      'Progressive Conservative',
      'New Democratic Party'
  ]

