from utils import CanadianJurisdiction


class Milton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3524009/council'
  geographic_code = 3524009

  def _get_metadata(self):
    return {
      'name': 'Milton',
      'legislature_name': 'Milton Town Council',
      'legislature_url': 'http://www.milton.ca',
    }
