from utils import CanadianJurisdiction

import re

class PointeClaire(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466097/council'
  geographic_code = 2466097
  def _get_metadata(self):
    return {
      'name': 'Pointe-Claire',
      'legislature_name': 'Pointe-Claire City Council',
      'legislature_url': 'http://www.ville.pointe-claire.qc.ca/en/city-hall-administration/your-council/municipal-council.html',
      'provides': ['people'],
    }
