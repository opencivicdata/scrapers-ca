from utils import CanadianJurisdiction


class Manitoba(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:mb/legislature'

  def _get_metadata(self):
    return {
      'name': 'Manitoba',
      'legislature_name': 'Manitoba City Council',
      'legislature_url': 'http://web5.gov.mb.ca/Public/municipalities.aspx',
    }
