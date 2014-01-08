from utils import CanadianJurisdiction


class Gatineau(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2481017/council'
  geographic_code = 2481017

  def _get_metadata(self):
    return {
      'division_name': 'Gatineau',
      'name': 'Conseil municipal de Gatineau',
      'url': 'http://www.gatineau.ca',
    }
