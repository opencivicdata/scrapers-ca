from utils import CanadianJurisdiction

class Senneville(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466127/council'
  geographic_code = 2466127
  def _get_metadata(self):
    return {
      'name': 'Senneville',
      'legislature_name': 'Senneville City Council',
      'legislature_url': 'http://www.villagesenneville.qc.ca/fr/membres-du-conseil-municipal',
      'provides': ['people'],
    }
