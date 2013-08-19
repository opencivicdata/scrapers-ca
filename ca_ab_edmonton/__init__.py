from utils import CanadianJurisdiction

class Burlington(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3524002/council'
  geographic_code = 4811061
  def _get_metadata(self):
    return {
      'name': 'Edmonton',
      'legislature_name': 'Edmonton City Council',
      'legislature_url': 'http://www.edmonton.ca/city_government/city_organization/city-councillors.aspx',
    }
