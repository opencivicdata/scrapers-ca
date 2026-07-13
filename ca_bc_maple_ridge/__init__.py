from pupa.scrape import Organization

from utils import CanadianJurisdiction


class MapleRidge(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5915075"
    division_name = "Maple Ridge"
    name = "Maple Ridge City Council"
    url = "https://www.mapleridge.ca"

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
