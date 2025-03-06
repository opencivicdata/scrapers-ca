from utils import CanadianJurisdiction

class CanadaCandidates(CanadianJurisdiction):
    classification = "executive"
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Parliament of Canada"
    url = "http://www.parl.gc.ca"
    parties = [{"name": "Liberal Party"}, {"name": "Conservative Party"}, {"name": "Bloc Québécois"}, {"name": "New Democratic Party"}, {"name": "Green Party"}, {"name": "Independent"}]


    # do i need a get_organization function ??
