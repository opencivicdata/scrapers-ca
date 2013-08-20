from utils import CanadianJurisdiction


class Brossard(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2458007/council'
  geographic_code = 2458007

  def _get_metadata(self):
    return {
      'name': 'Brossard',
      'legislature_name': 'Conseil municipal de Brossard',
      'legislature_url': 'http://www.ville.brossard.qc.ca',
    }
