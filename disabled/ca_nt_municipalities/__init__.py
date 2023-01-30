from utils import CanadianJurisdiction


# The official government sources lists only top-level officials.
# @see http://www.maca.gov.nt.ca/
class NorthwestTerritoriesMunicipalities(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/territory:nt"
    division_name = "Northwest Territories"
    name = "Northwest Territories Municipalities"
    url = "http://www.nwtac.com/about/communities/"
