from utils import CanadianJurisdiction


class Saguenay(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:2494068/council'
  geographic_code = 2494068

  def _get_metadata(self):
    return {
      'division_name': 'Saguenay',
      'name': 'Conseil municipal de Saguenay',
      'url': 'http://ville.saguenay.ca',
    }
