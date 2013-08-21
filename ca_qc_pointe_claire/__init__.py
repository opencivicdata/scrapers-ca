from utils import CanadianJurisdiction


class PointeClaire(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466097/council'
  geographic_code = 2466097

  def _get_metadata(self):
    return {
      'name': 'Pointe-Claire',
      'legislature_name': 'Conseil municipal de Pointe-Claire',
      'legislature_url': 'http://www.ville.pointe-claire.qc.ca',
    }
