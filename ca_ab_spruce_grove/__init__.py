from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SpruceGrove(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4811049"
    division_name = "Spruce Grove"
    name = "Spruce Grove City Council"
    url = "https://www.sprucegrove.org"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Spruce Grove", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Spruce Grove (seat {i})", division_id=self.division_id)
        yield organization
