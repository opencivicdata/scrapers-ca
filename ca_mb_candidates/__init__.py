from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class ManitobaCandidates(CanadianJurisdiction):
    classification = "executive"  # just to avoid clash
    division_id = "ocd-division/country:ca/province:mb"
    division_name = "Manitoba"
    name = "Manitoba Election Candidates"
    url = "https://www.gov.mb.ca/"
    parties = [
        {"name": "Green Party"},
        {"name": "Independant"},
        {"name": "Liberal"},
        {"name": "NDP"},
        {"name": "Progressive Conservative"},
    ]
    skip_null_valid_from = True
    valid_from = "2019-09-10"
    member_role = "candidate"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children("ed"):
            if division.attrs["validFrom"] == "2019-09-10":
                organization.add_post(role="candidate", label=division.name)

        yield organization
