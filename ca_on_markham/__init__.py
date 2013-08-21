from utils import CanadianJurisdiction


class Markham(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3519036/council'
  geographic_code = 3519036

  def _get_metadata(self):
    return {
      'name': 'Markham',
      'legislature_name': 'Markham City Council',
      'legislature_url': 'http://www.markham.ca',
    }
