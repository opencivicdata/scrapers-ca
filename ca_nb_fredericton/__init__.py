from utils import CanadianJurisdiction


class Fredericton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:1310032/council'
  geographic_code = 1310032

  def _get_metadata(self):
    return {
      'name': 'Fredericton',
      'legislature_name': 'Fredericton City Council',
      'legislature_url': 'http://www.fredericton.ca',
    }
