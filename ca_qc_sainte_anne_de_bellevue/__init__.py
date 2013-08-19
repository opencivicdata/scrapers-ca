from utils import CanadianJurisdiction

class SainteAnneDeBellevue(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466117/council'
  geographic_code = 2466117
  def _get_metadata(self):
    return {
      'name': 'Sainte-Anne-de-Bellevue',
      'legislature_name': 'Conseil municipal de Sainte-Anne-de-Bellevue',
      'legislature_url': 'http://www.ville.sainte-anne-de-bellevue.qc.ca/Democratie.aspx',
    }
