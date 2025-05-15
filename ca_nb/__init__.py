from utils import CanadianJurisdiction


class NewBrunswick(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:nb"
    division_name = "New Brunswick"
    name = "Legislative Assembly of New Brunswick"
    url = "https://www.legnb.ca/"
    parties = [
        {"name": "Green Party"},
        {"name": "Independent"},
        {"name": "Liberal Party"},
        {"name": "Progressive Conservative Party"},
    ]
