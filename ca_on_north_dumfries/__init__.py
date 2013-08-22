from utils import CanadianJurisdiction


class North_Dumfries(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3530004/council'
  geographic_code = 3530004

  def _get_metadata(self):
    return {
      'name': 'North Dumfries',
      'legislature_name': 'North Dumfries City Council',
      'legislature_url': 'http://www.northdumfries.ca/en/ourtownship/MeetYourCouncil.asp',
    }
