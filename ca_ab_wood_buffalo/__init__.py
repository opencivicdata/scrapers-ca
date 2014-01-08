from utils import CanadianJurisdiction


class WoodBuffalo(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:4816037/council'
  geographic_code = 4816037

  def _get_metadata(self):
    return {
      'division_name': 'Wood Buffalo',
      'name': 'Wood Buffalo Municipal Council',
      'url': 'http://www.woodbuffalo.ab.ca',
    }
