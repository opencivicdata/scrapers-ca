from utils import CanadianJurisdiction


class Summerside(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:1103025/council'
  geographic_code = 1103025

  def _get_metadata(self):
    return {
      'name': 'Summerside',
      'legislature_name': 'Summerside City Council',
      'legislature_url': 'http://www.city.summerside.pe.ca',
    }
