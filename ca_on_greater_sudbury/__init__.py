from utils import CanadianJurisdiction


class GreaterSudbury(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3553005/council'
  geographic_code = 3553005

  def _get_metadata(self):
    return {
      'name': 'Greater Sudbury',
      'legislature_name': 'Greater Sudbury City Council',
      'legislature_url': 'http://www.greatersudbury.ca',
    }
