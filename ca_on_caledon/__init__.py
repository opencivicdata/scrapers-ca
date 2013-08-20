from utils import CanadianJurisdiction


class Caledon(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3521024/council'
  geographic_code = 3521024

  def _get_metadata(self):
    return {
      'name': 'Caledon',
      'legislature_name': 'Caledon Town Council',
      'legislature_url': 'http://www.town.caledon.on.ca/en/townhall/council.asp',
    }
