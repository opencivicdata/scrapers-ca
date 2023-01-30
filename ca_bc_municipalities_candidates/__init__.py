from utils import CanadianJurisdiction


class BritishColumbiaMunicipalitiesCandidates(CanadianJurisdiction):
    classification = "executive"  # just to avoid clash
    division_id = "ocd-division/country:ca/province:bc"
    division_name = "British Columbia"
    name = "British Columbia municipal councils"
    url = "http://civicinfo.bc.ca"

    def get_organizations(self):
        return []
