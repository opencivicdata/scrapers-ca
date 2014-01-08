from utils import CanadianJurisdiction


class Lambton(CanadianJurisdiction):
  jurisdiction_id = u'ca-on-lambton'

  def _get_metadata(self):
    return {
      'division_name': 'Lambton',
      'name': 'Lambton County Council',
      'url': 'http://www.lambtononline.ca/home/government/accessingcountycouncil/countycouncillors/Pages/default.aspx',
    }
