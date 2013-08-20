from utils import CanadianJurisdiction


class Markham(CanadianJurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519036/council'
  geographic_code = 3519036

  def _get_metadata(self):
    return {
      'name': 'Markham',
      'legislature_name': 'Markham City Council',
      'legislature_url': 'http://www.markham.ca/wps/portal/Markham/MunicipalGovernment/MayorAndCouncil/RegionalAndWardCouncillors/!ut/p/a1/04_Sj9CPykssy0xPLMnMz0vMAfGjzOJN_N2dnX3CLAKNgkwMDDw9XcJM_VwCDUMDDfULsh0VAfz7Fis!/',
    }
