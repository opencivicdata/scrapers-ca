from utils import CanadianJurisdiction


class AlbertaCandidates(CanadianJurisdiction):
    classification = 'executive'  # just to avoid clash
    division_id = 'ocd-division/country:ca/province:ab'
    division_name = 'Alberta'
    name = 'Alberta Candidates'
    url = 'http://civicinfo.ab.ca'

    def get_organizations(self):
        return []
