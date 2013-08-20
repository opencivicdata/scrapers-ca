from utils import CanadianJurisdiction


class Westmount(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466032/council'
  geographic_code = 2466032

  def _get_metadata(self):
    return {
      'name': 'Westmount',
      'legislature_name': 'Conseil municipal de Westmount',
      'legislature_url': 'http://www.westmount.org',
    }
