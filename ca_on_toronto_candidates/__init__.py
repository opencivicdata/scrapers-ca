from utils import CanadianJurisdiction


class TorontoCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:on'
    division_name = 'Toronto'
    name = 'Toronto City Council'
    url = 'http://www.toronto.ca'
    parties = [
        {'name': "Alliance Party of Ontario"},
        {'name': "Cultural Action Party of Ontario"},
        {'name': "Canadians' Choice Party"},
        {'name': "Communist Party of Canada (Ontario)"},
        {'name': "Equal Parenting Party"},
        {'name': "Freedom Party of Ontario"},
        {'name': "Green Party of Ontario"},
        {'name': "New Democratic Party of Ontario"},
        {'name': "None of the Above Direct Democracy Party"},
        {'name': "Northern Ontario Party"},
        {'name': "Ontario Liberal Party"},
        {'name': "Ontario Libretarian Party"},
        {'name': "Ontario Moderate Party"},
        {'name': "Ontario Provincial Confederation of Regions Party"},
        {'name': "Party for People with Special Needs"},
        {'name': "Pauper Party of Ontario"},
        {'name': "Progressive Conservative Party of Ontario"},
        {'name': "Stop the New Sex-Ed Agenda"},
        {'name': "The Peoples Political Party"},
        {'name': "Trillium Party of Ontario"},
        {'name': "Vegan Environmental Party"},
        {'name': "Independent"},
    ]
    skip_null_valid_from = True
    valid_from = '2018-09-19'
    member_role = 'candidate'
