from pupa.scrape import Organization

from utils import CanadianJurisdiction


class ThunderBay(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3558004"
    division_name = "Thunder Bay"
    name = "Thunder Bay City Council"
    url = "http://www.thunderbay.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 6):
            organization.add_post(
                role="Councillor at Large",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )
        for ward_number, ward_name in enumerate(
            ("Current River", "Red River", "McKellar", "McIntyre", "Northwood", "Westfort", "Neebing"), 1
        ):
            organization.add_post(
                role="Councillor", label=ward_name, division_id=f"{self.division_id}/ward:{ward_number}"
            )

        yield organization
