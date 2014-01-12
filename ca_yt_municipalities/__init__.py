from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class Yukon(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/territory:yt/municipalities'
  division_name = 'Yukon'
  name = 'Yukon Municipalities'
  url = 'http://www.community.gov.yk.ca/pdf/loc_govdir.pdf'
