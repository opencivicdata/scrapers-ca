from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Yellowknife(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:6106023"
    division_name = "Yellowknife"
    name = "Yellowknife City Council"
    url = "https://www.yellowknife.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"Yellowknife (seat {i})", division_id=self.division_id)
        yield organization
