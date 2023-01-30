from utils import CanadianJurisdiction


class CanadaCandidates(CanadianJurisdiction):
    classification = "executive"  # just to avoid clash
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Parliament of Canada"
    url = "http://www.parl.gc.ca"
    parties = [
        {"name": "Alliance of the North"},
        {"name": "Animal Alliance Environment Voters"},
        {"name": "Bloc Québécois"},
        {"name": "Bridge"},
        {"name": "Canada"},
        {"name": "Canadian Action"},
        {"name": "Christian Heritage"},
        {"name": "Conservative"},
        {"name": "Co-operative Commonwealth Federation"},
        {"name": "Democratic Advancement"},
        {"name": "Forces et Démocratie"},
        {"name": "Green Party"},
        {"name": "Independent"},
        {"name": "Liberal"},
        {"name": "Libertarian"},
        {"name": "Marijuana"},
        {"name": "Marxist-Leninist Party of Canada"},
        {"name": "NDP"},
        {"name": "Party for Accountability, Competency and Transparency"},
        {"name": "Pirate"},
        {"name": "Progressive Canadian"},
        {"name": "Québec debout"},
        {"name": "Rhinoceros"},
        {"name": "Seniors"},
        {"name": "United"},
        {"name": "People's Party"},
        {"name": "Communist Party of Canada"},
        {"name": "Animal Protection Party of Canada"},
    ]
    skip_null_valid_from = True
    valid_from = "2019-05-31"
    member_role = "candidate"
