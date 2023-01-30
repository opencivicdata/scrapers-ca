from utils import CanadianJurisdiction


# The official government source only lists top-level officials.
# @see http://www.gov.ns.ca/snsmr/municipal/government/contact.asp
class NovaScotiaMunicipalities(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:ns"
    division_name = "Nova Scotia"
    name = "Nova Scotia Municipalities"
    url = "http://www.unsm.ca/doc_download/880-mayor-list-2013"
