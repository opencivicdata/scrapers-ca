from utils import CanadianJurisdiction


class Stratford(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:1102080/council'
  geographic_code = 1102080

  def _get_metadata(self):
    return {
      'name': 'Stratford',
      'legislature_name': 'Stratford Town Council',
      'legislature_url': 'http://www.townofstratford.ca',
    }
