from utils import CanadianJurisdiction


class Moncton(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:1307022/council'
  geographic_code = 1307022

  def _get_metadata(self):
    return {
      'name': 'Moncton',
      'legislature_name': 'Moncton City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
    }
