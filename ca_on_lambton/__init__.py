from utils import CanadianJurisdiction

class Lambton(CanadianJurisdiction):
  jurisdiction_id = 'ca-on-lambton'

  def _get_metadata(self):
    return {
      'name': 'Lambton',
      'legislature_name': 'Lambton County Council',
      'legislature_url': 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx',
      'provides': ['people'],
    }
