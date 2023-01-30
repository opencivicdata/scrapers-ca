from utils import CanadianJurisdiction


class Alberta(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:ab"
    division_name = "Alberta"
    name = "Legislative Assembly of Alberta"
    url = "https://www.assembly.ab.ca"
    parties = [
        {"name": "Alberta Liberal Party"},
        {"name": "Alberta New Democratic Party"},
        {"name": "Alberta Party"},
        {"name": "Freedom Conservative Party"},
        {"name": "Independent Conservative"},
        {"name": "Progressive Conservative Association of Alberta"},
        {"name": "United Conservative Party"},
        {"name": "Wildrose Alliance Party"},
        {"name": "Independent"},
    ]
    skip_null_valid_from = True
    valid_from = "2019-05-31"
