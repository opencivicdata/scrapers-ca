from utils import CanadianJurisdiction


class Saskatoon(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:4711066/council'
  geographic_code = 4711066

  def _get_metadata(self):
    return {
      'name': 'Saskatoon',
      'legislature_name': 'Saskatoon City Council',
      'legislature_url': "http://www.saskatoon.ca",
    }
