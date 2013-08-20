from utils import CanadianJurisdiction


class RichmondHill(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3519038/council'
  geographic_code = 3519038

  def _get_metadata(self):
    return {
      'name': 'Richmond Hill',
      'legislature_name': 'Richmond Hill Town Council',
      'legislature_url': 'http://www.town.richmond-hill.on.ca',
    }
