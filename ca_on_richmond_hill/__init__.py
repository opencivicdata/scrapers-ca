from utils import CanadianJurisdiction

class RichmondHill(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519038/council'
  geographic_code = 3519038
  def _get_metadata(self):
    return {
      'name': 'Richmond Hill',
      'legislature_name': 'Richmond Hill City Council',
      'legislature_url': 'http://www.richmondhill.ca/subpage.asp?pageid=townhall_members_of_the_council',
      'provides': ['people'],
    }
