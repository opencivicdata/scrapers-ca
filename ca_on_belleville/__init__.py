from utils import CanadianJurisdiction


class Belleville(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3512005/council'
  geographic_code = 3512005

  def _get_metadata(self):
    return {
      'division_name': 'Belleville',
      'name': 'Belleville City Council',
      'url': 'http://www.city.belleville.on.ca',
    }
