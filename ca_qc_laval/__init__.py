from utils import CanadianJurisdiction


class Laval(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2465005"
    division_name = "Laval"
    name = "Conseil municipal de Laval"
    url = "http://www.ville.laval.qc.ca"
    parties = [
        {"name": "Action Laval"},
        {"name": "Independant"},
        {"name": "Mouvement lavallois"},
        {"name": "Parti Laval"},
    ]
