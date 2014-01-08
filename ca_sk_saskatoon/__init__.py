from utils import CanadianJurisdiction


class Saskatoon(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/csd:4711066/council'
  geographic_code = 4711066

  def _get_metadata(self):
    return {
      'division_name': 'Saskatoon',
      'name': 'Saskatoon City Council',
      'url': "http://www.saskatoon.ca",
    }
