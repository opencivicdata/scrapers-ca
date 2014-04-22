# coding: utf-8
from utils import CanadianJurisdiction


class Ontario(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:on/legislature'
  geographic_code = 35
  division_name = u'Ontario'
  name = u'Legislative Assembly of Ontario'
  url = 'http://www.ontla.on.ca'
  parties = [
      'Ontario Liberal Party',
      'New Democratic Party of Ontario',
      'Progressive Conservative Party of Ontario'
  ]
