from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Timmins(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3556027"
    division_name = "Timmins"
    name = "Timmins City Council"
    url = "https://www.timmins.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Timmins", division_id=self.division_id)
        for i in range(1, 5):
            organization.add_post(role="Councillor", label=f"Ward {i}", division_id=self.division_id)
        for i in range(1, 5):
            organization.add_post(role="Councillor", label=f"Ward 5 (seat {i})", division_id=self.division_id)
        yield organization
