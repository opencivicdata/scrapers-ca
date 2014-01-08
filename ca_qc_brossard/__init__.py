from utils import CanadianJurisdiction


class Brossard(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2458007/council'
  geographic_code = 2458007

  def _get_metadata(self):
    return {
      'division_name': 'Brossard',
      'name': 'Conseil municipal de Brossard',
      'url': 'http://www.ville.brossard.qc.ca',
    }
