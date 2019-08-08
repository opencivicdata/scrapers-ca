from utils import CanadianJurisdiction


class ManitobaCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:mb'
    division_name = 'Manitoba'
    name = 'Manitoba Election Candidates'
    url = 'https://www.gov.mb.ca/'
    parties = [
        {'name': "Green Party"},
        {'name': "Independant"},
        {'name': "Liberal"},
        {'name': "NDP"},
        {'name': "Progressive Conservative"},
    ]
    skip_null_valid_from = True
    valid_from = '2019-07-08'
    member_role = 'candidate'
