from utils import CanadianJurisdiction


class Burlington(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3524002/council'
  geographic_code = 3524002

  def _get_metadata(self):
    return {
      'division_name': 'Burlington',
      'name': 'Burlington City Council',
      'url': 'http://cms.burlington.ca',
    }
