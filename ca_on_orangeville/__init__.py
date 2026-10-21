from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Orangeville(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3522014"
    division_name = "Orangeville"
    name = "Orangeville Town Council"
    url = "https://www.orangeville.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Deputy Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 6):
            organization.add_post(
                role="Councillor", label=f"Orangeville (seat {seat_number})", division_id=self.division_id
            )
        yield organization
