from pupa.scrape import Organization

from utils import CanadianJurisdiction


class FortErie(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3526003"
    division_name = "Fort Erie"
    name = "Fort Erie Town Council"
    url = "https://www.forterie.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 7):
            organization.add_post(role="Councillor", label=f"Ward {ward_number}", division_id=self.division_id)

        yield organization
