from utils import CanadianJurisdiction

class PrinceEdwardIsland(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:pe/legislature'

  def _get_metadata(self):
    return {
      'name': 'British Columbia',
      'legislature_name': 'British Columbia Legislative Assembly',
      'legislature_url': 'http://www.leg.bc.ca/mla/3-2.htm',
    }
