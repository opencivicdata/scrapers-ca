from utils import CanadianJurisdiction


class BritishColumbia(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:bc"
    division_name = "British Columbia"
    name = "Legislative Assembly of British Columbia"
    url = "http://www.leg.bc.ca"
    parties = [
        {"name": "Conservative Party of British Columbia"},
        {"name": "British Columbia New Democratic Party"},
        {"name": "British Columbia Liberal Party"},
        {"name": "British Columbia Green Party"},
        {"name": "BC United"},
        {"name": "Independent"},
    ]
    skip_null_valid_from = True
    valid_from = "2024-10-19"
