from utils import CanadianJurisdiction


class QuebecCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:qc'
    division_name = 'Québec'
    name = 'Assemblée nationale du Québec'
    url = 'http://www.assnat.qc.ca'
    parties = [
        {'name': u'Coalition avenir Québec'},
        {'name': u'Parti québécois'},
        {'name': u'Parti libéral du Québec'},
        {'name': u'Parti vert du Québec'},
        {'name': u'Québec solidaire'},
    ]
    skip_null_valid_from = True
    valid_from = '2018-10-01'
    member_role = 'candidate'
