# coding: utf-8
from utils import CanadianJurisdiction


class NewBrunswick(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:nb/legislature'
  geographic_code = 13
  division_name = u'New Brunswick'
  name = u'Legislative Assembly of New Brunswick'
  url = 'http://www.gnb.ca/legis/index.asp'
  parties = [
      {'name': u'Progressive Conservative Party of New Brunswick'},
      {'name': 'New Brunswick Liberal Association'},
      {'name': 'Independent}'},
  ]
