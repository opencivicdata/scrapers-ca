from utils import CanadianJurisdiction


class NorthwestTerritories(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/territory:nt/legislature'

  def _get_metadata(self):
    return {
      'name': 'Northwest Territories',
      'legislature_name': 'Northwest Territories City Council',
      'legislature_url': 'http://www.nwtac.com/about/communities/',
    }
