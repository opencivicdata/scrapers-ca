from utils import CanadianJurisdiction

class ChathamKent(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3536020/council'
  geographic_code = 3536020
  def _get_metadata(self):
    return {
      'name': 'Chatham-Kent',
      'legislature_name': 'Chatham-Kent City Council',
      'legislature_url': 'http://www.chatham-kent.ca/Council/councilmembers/Pages/CouncilMembers.aspx',
      'provides': ['people'],
    }
