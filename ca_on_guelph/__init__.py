from utils import CanadianJurisdiction


class Guelph(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3523008/council'
  geographic_code = 3523008

  def _get_metadata(self):
    return {
      'name': 'Guelph',
      'legislature_name': 'Guelph City Council',
      'legislature_url': 'http://guelph.ca',
    }
