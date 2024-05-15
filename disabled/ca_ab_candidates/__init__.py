from utils import CanadianJurisdiction


class AlbertaCandidates(CanadianJurisdiction):
    classification = "executive"  # just to avoid clash
    division_id = "ocd-division/country:ca/province:ab"
    division_name = "Alberta"
    name = "Alberta Election Candidates"
    url = "http://www.assembly.ab.ca/"
    parties = [
        {"name": "Alberta Advantage Party"},
        {"name": "Alberta Liberal Party"},
        {"name": "Alberta New Democratic Party"},
        {"name": "Alberta Party"},
        {"name": "Freedom Conservative"},
        {"name": "Green Party of Alberta"},
        {"name": "Alberta Independance Party"},
        {"name": "United Conservative Party"},
    ]
    skip_null_valid_from = True
    valid_from = "2019-05-31"
    member_role = "candidate"
