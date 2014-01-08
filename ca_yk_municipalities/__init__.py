from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class Yukon(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:yk/legislature'

  def _get_metadata(self):
    return {
      'division_name': 'Yukon',
      'name': 'Yukon Municipal Legislation',
      'url': 'http://www.community.gov.yk.ca/pdf/loc_govdir.pdf',
    }
