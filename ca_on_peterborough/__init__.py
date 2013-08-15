from utils import CanadianJurisdiction

class Peterborough(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3515014/council'
  geographic_code = 3515014
  def _get_metadata(self):
    return {
      'name': 'Peterborough',
      'legislature_name': 'Peterborough City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
      'provides': ['people'],
    }
