from utils import CanadianJurisdiction


# The municipal association lists only top-level officials.
# @see http://www.municipalnl.ca/?Content=Contact/Municipal_Directory
class NewfoundlandAndLabradorMunicipalities(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:nl"
    division_name = "Newfoundland and Labrador"
    name = "Newfoundland and Labrador Municipalities"
    url = "http://www.ma.gov.nl.ca/ma/municipal_directory/index.html"
