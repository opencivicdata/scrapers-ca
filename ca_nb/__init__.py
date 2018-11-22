from utils import CanadianJurisdiction


class NewBrunswick(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/province:nb'
    division_name = 'New Brunswick'
    name = 'Legislative Assembly of New Brunswick'
    url = 'http://www.gnb.ca/legis/index.asp'
    parties = [
        {'name': 'Green Party'},
        {'name': 'Independent'},
        {'name': 'New Brunswick Liberal Association'},
        {'name': "People's Alliance"},
        {'name': 'Progressive Conservative Party of New Brunswick'},
    ]
