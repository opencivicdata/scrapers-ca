from utils import CanadianJurisdiction


class BritishColumbia(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:bc/legislature'
  geographic_code = 59
  division_name = 'British Columbia'
  name = 'Legislative Assembly of British Columbia'
  url = 'http://www.leg.bc.ca'
  parties = [
    {'name': 'New Democratic Party of British Columbia'},
    {'name': 'British Columbia Liberal Party'},
  ]
