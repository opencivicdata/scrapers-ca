from utils import CanadianJurisdiction


class KawarthaLakes(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:3516010/council'
  geographic_code = 3516010

  def _get_metadata(self):
    return {
      'name': 'Kawartha Lakes',
      'legislature_name': 'Kawartha Lakes City Council',
      'legislature_url': 'http://www.city.kawarthalakes.on.ca',
    }
