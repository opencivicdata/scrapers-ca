from utils import CanadianJurisdiction


# The official government sources lists only top-level officials.
# @see http://www.maca.gov.nt.ca/
class NorthwestTerritoriesMunicipalities(CanadianJurisdiction):
  jurisdiction_id = u'ocd-jurisdiction/country:ca/territory:nt/municipalities'
  geographic_code = 61
  division_name = 'Northwest Territories'
  name = 'Northwest Territories Municipalities'
  url = 'http://www.nwtac.com/about/communities/'
