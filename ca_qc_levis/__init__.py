from utils import CanadianJurisdiction


class Levis(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2425213/council'
  geographic_code = 2425213

  def _get_metadata(self):
    return {
      'name': 'Levis',
      'legislature_name': 'Levis City Council',
      'legislature_url': 'http://www.ville.levis.qc.ca/Fr/Conseil/',
    }
