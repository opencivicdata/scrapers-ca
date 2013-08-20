from utils import CanadianJurisdiction


class Saskatoon(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4711066/council'
  geographic_code = 4711066

  def _get_metadata(self):
    return {
      'name': 'Saskatoon',
      'legislature_name': 'Saskatoon City Council',
      'legislature_url': "http://www.saskatoon.ca/CITY%20COUNCIL/YOUR%20WARD%20COUNCILLORS/Pages/default.aspx",
    }
