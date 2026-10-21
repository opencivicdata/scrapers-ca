from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Airdrie(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4806021"
    division_name = "Airdrie"
    name = "Airdrie City Council"
    url = "https://www.airdrie.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 7):
            organization.add_post(
                role="Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )

        yield organization
