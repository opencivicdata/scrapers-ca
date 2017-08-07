from utils import CanadianJurisdiction


class Alberta(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:ab'
    division_name = 'Alberta'
    name = 'Legislative Assembly of Alberta'
    url = 'https://www.assembly.ab.ca'
    parties = [
        {'name': 'Alberta Party'},
        {'name': 'Alberta Liberal Party'},
        {'name': 'Alberta New Democratic Party'},
        {'name': 'Progressive Conservative Association of Alberta'},
        {'name': 'Wildrose Alliance Party'},
        {'name': 'United Conservative'},
        {'name': 'Independent'},
    ]
