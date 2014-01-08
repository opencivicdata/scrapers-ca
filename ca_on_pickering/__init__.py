from utils import CanadianJurisdiction


class Pickering(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3518001/council'
  geographic_code = 3518001

  def _get_metadata(self):
    return {
      'name': 'Pickering',
      'legislature_name': 'Pickering City Council',
      'legislature_url': 'http://www.pickering.ca',
    }
