from utils import CanadianJurisdiction


class Manitoba(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:mb"
    division_name = "Manitoba"
    name = "Legislative Assembly of Manitoba"
    url = "http://www.gov.mb.ca/legislature/"
    parties = [
        {"name": "Independent"},
        {"name": "Independent Liberal"},
        {"name": "Manitoba Liberal Party"},
        {"name": "Manitoba Party"},
        {"name": "New Democratic Party of Manitoba"},
        {"name": "Progressive Conservative Party of Manitoba"},
    ]
    skip_null_valid_from = True
    valid_from = "2019-09-10"
