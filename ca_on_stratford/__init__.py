from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Stratford(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3531011"
    division_name = "Stratford"
    name = "Stratford City Council"
    url = "https://www.stratford.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 11):
            organization.add_post(
                role="Councillor", label=f"Stratford (seat {seat_number})", division_id=self.division_id
            )
        yield organization
