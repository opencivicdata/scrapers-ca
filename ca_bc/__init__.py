from utils import CanadianJurisdiction


class BritishColumbia(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:pe/legislature'

  def _get_metadata(self):
    return {
      'name': 'British Columbia',
      'legislature_name': 'British Columbia Legislative Assembly',
      'legislature_url': 'http://www.leg.bc.ca/mla/3-2.htm',
    }
