from utils import CanadianJurisdiction


class NewfoundlandAndLabrador(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:nl"
    division_name = "Newfoundland and Labrador"
    name = "Newfoundland and Labrador House of Assembly"
    url = "http://www.assembly.nl.ca"
    parties = [
        {"name": "Progressive Conservative Party of Newfoundland and Labrador"},
        {"name": "New Democratic Party of Newfoundland and Labrador"},
        {"name": "Liberal Party of Newfoundland and Labrador"},
        {"name": "Independent"},
    ]
