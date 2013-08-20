from utils import CanadianJurisdiction


class StCatharines(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3526053/council'
  geographic_code = 3526053

  def _get_metadata(self):
    return {
      'name': 'St. Catharines',
      'legislature_name': 'St. Catharines City Council',
      'legislature_url': 'http://www.stcatharines.ca/en/governin/BrianMcMullanMayor.asp',
    }
