from utils import CanadianJurisdiction

class CoteSaintLuc(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466058/council'
  geographic_code = 2466058
  def _get_metadata(self):
    return {
      'name': 'Cote_St-Luc',
      'legislature_name': 'Cote St-Luc City Council',
      'legislature_url': 'http://www.cotesaintluc.org/Administration',
      'provides': ['people'],
    }
