from utils import CanadianJurisdiction

class Clarington(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3518017/council'
  geographic_code = 3518017
  def _get_metadata(self):
    return {
      'name': 'Clarington',
      'legislature_name': 'Clarington City Council',
      'legislature_url': 'http://www.clarington.net/htdocs/council_bios.html',
      'provides': ['people'],
    }
