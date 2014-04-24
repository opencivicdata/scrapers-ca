# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class NovaScotia(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:ns/legislature'
  geographic_code = 12
  division_name = 'Nova Scotia'
  name = 'Nova Scotia House of Assembly'
  url = 'http://nslegislature.ca/'
  parties = [
    {'name': 'Nova Scotia Liberal Party'},
    {'name': 'Progressive Conservative Association of Nova Scotia'},
    {'name': 'Nova Scotia New Democratic Party'},
  ]
