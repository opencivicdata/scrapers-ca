from utils import CanadianJurisdiction

class SaintJerome(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2475017/council'
  geographic_code = 2475017
  def _get_metadata(self):
    return {
      'name': 'Sainte-Jerome',
      'legislature_name': 'Sainte-Jerome City Council',
      'legislature_url': 'http://www.ville.saint-jerome.qc.ca/pages/aSavoir/conseilMunicipal.aspx',
      'provides': ['people'],
    }
