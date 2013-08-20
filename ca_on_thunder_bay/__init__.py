from utils import CanadianJurisdiction


class ThunderBay(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3558004/council'
  geographic_code = 3558004

  def _get_metadata(self):
    return {
      'name': 'Thunder Bay',
      'legislature_name': 'Thunder Bay City Council',
      'legislature_url': 'http://www.thunderbay.ca',
    }
