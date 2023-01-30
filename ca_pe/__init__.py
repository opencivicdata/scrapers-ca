from utils import CanadianJurisdiction


class PrinceEdwardIsland(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:pe"
    division_name = "Prince Edward Island"
    name = "Legislative Assembly of Prince Edward Island"
    url = "http://www.assembly.pe.ca"
    parties = [
        {"name": "Liberal Party of Prince Edward Island"},
        {"name": "Green Party of Prince Edward Island"},
        {"name": "Progressive Conservative Party of Prince Edward Island"},
    ]
