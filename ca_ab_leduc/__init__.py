from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Leduc(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4811016"
    division_name = "Leduc"
    name = "Leduc City Council"
    url = "https://www.leduc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 7):
            organization.add_post(role="Councillor", label=f"Leduc (seat {seat_number})", division_id=self.division_id)
        yield organization
