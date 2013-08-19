from utils import CanadianJurisdiction

class Gatineau(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2481017/council'
  geographic_code = 2481017
  def _get_metadata(self):
    return {
      'name': 'Gatineau',
      'legislature_name': 'Conseil municipal de Gatineau',
      'legislature_url': 'http://www.gatineau.ca/page.asp?p=la_ville/conseil_municipal',
    }
