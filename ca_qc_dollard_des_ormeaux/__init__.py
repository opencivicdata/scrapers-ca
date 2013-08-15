from utils import CanadianJurisdiction

class DollardDesOrmeaux(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466142/council'
  geographic_code = 2466142
  def _get_metadata(self):
    return {
      'name': 'Dollard-Des-Ormeaux',
      'legislature_name': 'Dollard-Des-Ormeaux City Council',
      'legislature_url': 'http://www.ville.ddo.qc.ca/en/default.asp?contentID=17',
    }
