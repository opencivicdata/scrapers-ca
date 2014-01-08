from utils import CanadianJurisdiction


class Westmount(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2466032/council'
  geographic_code = 2466032

  def _get_metadata(self):
    return {
      'division_name': 'Westmount',
      'name': 'Conseil municipal de Westmount',
      'url': 'http://www.westmount.org',
    }
