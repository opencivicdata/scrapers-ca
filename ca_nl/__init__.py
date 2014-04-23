# coding: utf-8
from utils import CanadianJurisdiction


class NewfoundlandAndLabrador(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:nl/legislature'
  geographic_code = 10
  division_name = u'Newfoundland and Labrador'
  name = u'Newfoundland and Labrador House of Assembly'
  url = 'http://www.assembly.nl.ca'
  parties = [
      {'name': u'Progressive Conservative Party of Newfoundland and Labrador'},
      {'name': u'New Democratic Party of Newfoundland and Labrador'},
      {'name': u'Liberal Party of Newfoundland and Labrador'},
  ]

