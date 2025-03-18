from utils import CanadianJurisdiction


class Saskatchewan(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:sk"
    division_name = "Saskatchewan"
    name = "Legislative Assembly of Saskatchewan"
    url = "http://www.legassembly.sk.ca"
    parties = [
        {"name": "Opposition Caucus"},
        {"name": "Government Caucus"},
    ]
    skip_null_valid_from = True
