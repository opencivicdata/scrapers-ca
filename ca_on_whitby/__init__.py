from utils import CanadianJurisdiction


class Whitby(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3518009/council'
  geographic_code = 3518009

  def _get_metadata(self):
    return {
      'division_name': 'Whitby',
      'name': 'Whitby Town Council',
      'url': 'http://www.whitby.ca',
    }
