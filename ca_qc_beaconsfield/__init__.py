from utils import CanadianJurisdiction


class Beaconsfield(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466107/council'
  geographic_code = 2466107

  def _get_metadata(self):
    return {
      'division_name': 'Beaconsfield',
      'name': 'Conseil municipal de Beaconsfield',
      'url': 'http://www.beaconsfield.ca',
    }
