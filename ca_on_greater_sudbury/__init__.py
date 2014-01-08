from utils import CanadianJurisdiction


class GreaterSudbury(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3553005/council'
  geographic_code = 3553005

  def _get_metadata(self):
    return {
      'division_name': 'Greater Sudbury',
      'name': 'Greater Sudbury City Council',
      'url': 'http://www.greatersudbury.ca',
    }
