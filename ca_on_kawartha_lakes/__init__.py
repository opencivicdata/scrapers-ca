from utils import CanadianJurisdiction


class KawarthaLakes(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3516010/council'
  geographic_code = 3516010

  def _get_metadata(self):
    return {
      'division_name': 'Kawartha Lakes',
      'name': 'Kawartha Lakes City Council',
      'url': 'http://www.city.kawarthalakes.on.ca',
    }
