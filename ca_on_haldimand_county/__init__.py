from utils import CanadianJurisdiction


class HaldimandCounty(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3528018/council'
  geographic_code = 3528018

  def _get_metadata(self):
    return {
      'division_name': 'Haldimand County',
      'name': 'Haldimand County Council',
      'url': 'http://www.haldimandcounty.on.ca',
    }
