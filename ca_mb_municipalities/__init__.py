from utils import CanadianJurisdiction


class Manitoba(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:mb/legislature'

  def _get_metadata(self):
    return {
      'division_name': 'Manitoba',
      'name': 'Manitoba City Council',
      'url': 'http://web5.gov.mb.ca/Public/municipalities.aspx',
    }
