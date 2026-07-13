from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Mission(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5909056"
    division_name = "Mission"
    name = "Mission City Council"
    url = "https://www.mission.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Mission", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Mission (seat {i})", division_id=self.division_id)
        yield organization
