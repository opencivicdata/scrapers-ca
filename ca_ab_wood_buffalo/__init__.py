from utils import CanadianJurisdiction

class WoodBuffalo(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4816037/council'
  geographic_code = 4816037
  def _get_metadata(self):
    return {
      'name': 'Wood Buffalo',
      'legislature_name': 'Wood Buffalo City Council',
      'legislature_url': 'http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm',
    }
