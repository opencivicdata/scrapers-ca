from pupa.scrape import Organization

from utils import CanadianJurisdiction


class WestVancouver(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5915055"
    division_name = "West Vancouver"
    name = "West Vancouver District Council"
    url = "https://westvancouver.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="West Vancouver", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"West Vancouver (seat {i})", division_id=self.division_id)
        yield organization
