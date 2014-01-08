from utils import CanadianJurisdiction


class Saskatchewan(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/province:sk/legislature'
  geographic_code = 47

  def _get_metadata(self):
    return {
      'division_name': 'Saskatchewan',
      'name': 'Legislative Assembly of Saskatchewan',
      'url': 'http://www.legassembly.sk.ca',
    }
