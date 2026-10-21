from pupa.scrape import Organization

from utils import CanadianJurisdiction


class FortSaskatchewan(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4811056"
    division_name = "Fort Saskatchewan"
    name = "Fort Saskatchewan City Council"
    url = "https://www.fortsask.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat in range(1, 7):
            organization.add_post(
                role="Councillor", label=f"{self.division_name} (seat {seat})", division_id=self.division_id
            )
        yield organization
