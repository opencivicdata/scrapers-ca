from utils import CanadianJurisdiction


class Quebec(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:qc"
    division_name = "Québec"
    name = "Assemblée nationale du Québec"
    url = "http://www.assnat.qc.ca"
    parties = [
        {"name": "Parti libéral du Québec"},
        {"name": "Parti québécois"},
        {"name": "Parti conservateur du Québec"},
        {"name": "Coalition avenir Québec"},
        {"name": "Québec solidaire"},
        {"name": "Indépendant"},
    ]
    skip_null_valid_from = True
    valid_from = "2018-10-01"
