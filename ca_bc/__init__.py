from utils import CanadianJurisdiction


class BritishColumbia(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:bc/legislature'
  geographic_code = 59

  def _get_metadata(self):
    return {
      'division_name': 'British Columbia',
      'name': 'Legislative Assembly of British Columbia',
      'url': 'http://www.leg.bc.ca',
    }
