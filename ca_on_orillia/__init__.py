from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Orillia(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3543052"
    division_name = "Orillia"
    name = "Orillia City Council"
    url = "https://www.orillia.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 5):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=self.division_id,
                )
        yield organization
