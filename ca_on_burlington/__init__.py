from utils import CanadianJurisdiction


class Burlington(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3524002/council'
  geographic_code = 3524002

  def _get_metadata(self):
    return {
      'name': 'Burlington',
      'legislature_name': 'Burlington City Council',
      'legislature_url': 'http://cms.burlington.ca',
    }
