from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Canmore(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4815023"
    division_name = "Canmore"
    name = "Canmore Town Council"
    url = "https://www.canmore.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat in range(1, 7):
            organization.add_post(
                role="Councillor", label=f"{self.division_name} (seat {seat})", division_id=self.division_id
            )
        yield organization
