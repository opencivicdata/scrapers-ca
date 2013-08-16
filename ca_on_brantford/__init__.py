from utils import CanadianJurisdiction

class Brantford(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3529006/council'
  geographic_code = 3529006
  def _get_metadata(self):
    return {
      'name': 'Brantford',
      'legislature_name': 'Brantford City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
    }
