from utils import CanadianJurisdiction


class Wilmont(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530020/council'
  geographic_code = 3530020

  def _get_metadata(self):
    return {
      'name': 'Wilmont',
      'legislature_name': 'Wilmont City Council',
      'legislature_url': 'http://www.wilmot.ca/current-council.php',
    }
