from utils import CanadianJurisdiction


class Sherbrooke(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2443027/council'
  geographic_code = 2443027

  def _get_metadata(self):
    return {
      'name': 'Sherbrooke',
      'legislature_name': 'Sherbrooke City Council',
      'legislature_url': 'http://www.ville.sherbrooke.qc.ca/mairie-et-vie-democratique/conseil-municipal/elus-municipaux/',
    }
