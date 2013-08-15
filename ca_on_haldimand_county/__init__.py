from utils import CanadianJurisdiction

class HaldimandCounty(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3528018/council'
  geographic_code = 3528018
  def _get_metadata(self):
    return {
      'name': 'Haldimand County',
      'legislature_name': 'Haldimand County Council',
      'legislature_url': 'http://www.haldimandcounty.on.ca/OurCounty.aspx?id=338',
      'provides': ['people'],
    }
