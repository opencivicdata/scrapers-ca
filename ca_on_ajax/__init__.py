from utils import CanadianJurisdiction


class Ajax(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3518005/council'
  geographic_code = 3518005

  def _get_metadata(self):
    return {
      'division_name': 'Ajax',
      'name': 'Ajax Town Council',
      'url': 'http://www.ajax.ca',
    }
