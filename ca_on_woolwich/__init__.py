from utils import CanadianJurisdiction


class Woolwich(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530035/council'
  geographic_code = 3530035

  def _get_metadata(self):
    return {
      'division_name': 'Woolwich',
      'name': 'Woolwich Township Council',
      'url': 'http://www.woolwich.ca',
    }
