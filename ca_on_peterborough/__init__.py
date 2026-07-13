from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Peterborough(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3515014"
    division_name = "Peterborough"
    name = "Peterborough City Council"
    url = "https://www.peterborough.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        wards = [
            "Ward 1 - Otonabee",
            "Ward 2 - Monaghan",
            "Ward 3 - Town",
            "Ward 4 - Ashburnham",
            "Ward 5 - Northcrest",
        ]
        for ward_number, ward in enumerate(wards, start=1):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"{ward} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
