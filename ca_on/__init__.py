from utils import CanadianJurisdiction


class Ontario(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:on'
    division_name = 'Ontario'
    name = 'Legislative Assembly of Ontario'
    url = 'http://www.ontla.on.ca'
    parties = [
        {'name': 'Ontario Liberal Party'},
        {'name': 'New Democratic Party of Ontario'},
        {'name': 'Progressive Conservative Party of Ontario'},
        {'name': 'Independent'},
    ]
    skip_null_valid_from = True
