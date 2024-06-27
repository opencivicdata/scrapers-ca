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
        {"name": "Green Party of Alberta"},
        {"name": "Alberta Independance Party"},
        {"name": "United Conservative Party"},
        {"name": "Communist Party - Alberta"},
        {"name": "Pro-Life Alberta Political Association"},
        {"name": "Reform Party of Alberta"},
        {"name": "Solidarity Movement of Alberta"},
        {"name": "The Buffalo Party of Alberta"},
        {"name": "Wildrose Independence Party of Alberta"},
        {"name": "Wildrose Loyalty Coalition"},
        {"name": "No Party Affiliation"},
    ]
    skip_null_valid_from = True
    valid_from = "2023-01-05"
    member_role = "candidate"
