from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class YukonMunicipalities(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/territory:yt"
    division_name = "Yukon"
    name = "Yukon Municipalities"
    url = "http://www.community.gov.yk.ca/pdf/loc_govdir.pdf"
