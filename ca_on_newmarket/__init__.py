from utils import CanadianJurisdiction

class Newmarket(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519048/council'
  geographic_code = 3519048
  def _get_metadata(self):
    return {
      'name': 'Newmarket',
      'legislature_name': 'Newmarket City Council',
      'legislature_url': 'http://www.newmarket.ca/en/townhall/contactinformationmayorandtowncouncil.asp',
    }
