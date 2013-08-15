from utils import CanadianJurisdiction

class Dorval(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466087/council'
  geographic_code = 2466087
  def _get_metadata(self):
    return {
      'name': 'Dorval',
      'legislature_name': 'Dorval Municipal Council',
      'legislature_url': 'http://www.ville.dorval.qc.ca/en/default.asp?contentID=516',
      'provides': ['people'],
    }
