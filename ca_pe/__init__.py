from utils import CanadianJurisdiction

class PrinceEdwardIsland(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:pe/legislature'

  def _get_metadata(self):
    return {
      'name': 'Prince Edward Island',
      'legislature_name': 'Prince Edward Island City Council',
      'legislature_url': 'http://www.gov.pe.ca/mapp/municipalitites.php',
      'provides': ['people'],
    }
