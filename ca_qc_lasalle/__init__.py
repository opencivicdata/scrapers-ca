from utils import CanadianJurisdiction

class LaSalle(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-lasalle'

  def _get_metadata(self):
    return {
      'name': 'LaSalle',
      'legislature_name': 'LaSalle City Council',
      'legislature_url': 'http://www.town.lasalle.on.ca/Council/council-council.htm',
    }
