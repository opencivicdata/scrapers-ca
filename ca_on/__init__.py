# coding: utf-8
from __future__ import unicode_literals

from utils import CanadianJurisdiction


class Ontario(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:on/legislature'
  geographic_code = 35
  division_name = 'Ontario'
  name = 'Legislative Assembly of Ontario'
  url = 'http://www.ontla.on.ca'
  parties = [
    {'name': 'Ontario Liberal Party'},
    {'name': 'New Democratic Party of Ontario'},
    {'name': 'Progressive Conservative Party of Ontario'},
  ]
