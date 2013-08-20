from utils import CanadianJurisdiction


class CapeBreton(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:1217030/council'
  geographic_code = 1217030

  def _get_metadata(self):
    return {
      'name': 'Cape Breton',
      'legislature_name': 'Cape Breton Regional Council',
      'legislature_url': 'http://www.cbrm.ns.ca',
    }
