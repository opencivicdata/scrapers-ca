from utils import CanadianJurisdiction

class NewBrunswick(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:nb/legislature'
  geographic_code = 13
  def _get_metadata(self):
    return {
      'name': 'New Brunswick',
      'legislature_name': 'New Brunswick City Council',
      'legislature_url': 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html',
      'provides': ['people'],
    }
