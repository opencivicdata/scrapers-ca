from __future__ import unicode_literals

from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class YukonMunicipalities(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/territory:yt/municipalities'
  geographic_code = 60
  division_name = 'Yukon'
  name = 'Yukon Municipalities'
  url = 'http://www.community.gov.yk.ca/pdf/loc_govdir.pdf'
