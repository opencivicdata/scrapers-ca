from utils import CanadianJurisdiction


class CapeBreton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:1217030/council'
  geographic_code = 1217030

  def _get_metadata(self):
    return {
      'division_name': 'Cape Breton',
      'name': 'Cape Breton Regional Council',
      'url': 'http://www.cbrm.ns.ca',
    }
