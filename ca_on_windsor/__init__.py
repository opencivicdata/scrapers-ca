from utils import CanadianJurisdiction


class Windsor(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3537039/council'
  geographic_code = 3537039

  def _get_metadata(self):
    return {
      'name': 'Windsor',
      'legislature_name': 'Windsor City Council',
      'legislature_url': 'http://www.citywindsor.ca',
    }
