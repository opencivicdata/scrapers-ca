from utils import CanadianJurisdiction

class Ajax(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3518005/council'
  geographic_code = 3518005
  def _get_metadata(self):
    return {
      'name': 'Ajax',
      'legislature_name': 'Ajax City Council',
      'legislature_url': 'http://www.ajax.ca/en/insidetownhall/mayorcouncillors.asp',
    }
