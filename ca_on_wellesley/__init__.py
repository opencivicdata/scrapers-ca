from utils import CanadianJurisdiction


class Wellesley(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530027/council'
  geographic_code = 3530027

  def _get_metadata(self):
    return {
      'name': 'Wellesley',
      'legislature_name': 'Wellesley City Council',
      'legislature_url': 'http://www.township.wellesley.on.ca/index.php?file=council/council.html',
    }
