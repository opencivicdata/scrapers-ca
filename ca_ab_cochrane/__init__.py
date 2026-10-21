from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Cochrane(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4806019"
    division_name = "Cochrane"
    name = "Cochrane Town Council"
    url = "https://www.cochrane.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 7):
            organization.add_post(
                role="Councillor", label=f"Cochrane (seat {seat_number})", division_id=self.division_id
            )
        yield organization
