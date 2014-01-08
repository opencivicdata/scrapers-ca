from utils import CanadianJurisdiction


class Clarington(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3518017/council'
  geographic_code = 3518017

  def _get_metadata(self):
    return {
      'division_name': 'Clarington',
      'name': 'Clarington Municipal Council',
      'url': 'http://www.clarington.net',
    }
