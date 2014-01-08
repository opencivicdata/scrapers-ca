from utils import CanadianJurisdiction


class SainteAnneDeBellevue(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466117/council'
  geographic_code = 2466117

  def _get_metadata(self):
    return {
      'division_name': 'Sainte-Anne-de-Bellevue',
      'name': 'Conseil municipal de Sainte-Anne-de-Bellevue',
      'url': 'http://www.ville.sainte-anne-de-bellevue.qc.ca',
    }
