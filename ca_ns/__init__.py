from utils import CanadianJurisdiction


class NovaScotia(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:ns"
    division_name = "Nova Scotia"
    name = "Nova Scotia House of Assembly"
    url = "http://nslegislature.ca"
    parties = [
        {"name": "Nova Scotia Liberal Party"},
        {"name": "Progressive Conservative Association of Nova Scotia"},
        {"name": "Nova Scotia New Democratic Party"},
        {"name": "Independent"},
    ]
