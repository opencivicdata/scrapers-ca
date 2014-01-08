from utils import CanadianJurisdiction


class LaSalle(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3537034/council'
  geographic_code = 3537034

  def _get_metadata(self):
    return {
      'division_name': 'LaSalle',
      'name': 'LaSalle Town Council',
      'url': 'http://www.town.lasalle.on.ca',
    }
