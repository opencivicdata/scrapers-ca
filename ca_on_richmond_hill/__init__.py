from pupa.scrape import Organization

from utils import CanadianJurisdiction


class RichmondHill(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3519038"
    division_name = "Richmond Hill"
    name = "Richmond Hill Town Council"
    url = "http://www.town.richmond-hill.on.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 3):
            organization.add_post(
                role="Regional Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )
        for ward_number in range(1, 7):
            organization.add_post(
                role="Councillor",
                label=f"Ward {ward_number}",
                division_id=f"{self.division_id}/ward:{ward_number}",
            )

        yield organization
