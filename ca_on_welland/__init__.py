from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Welland(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3526032"
    division_name = "Welland"
    name = "Welland City Council"
    url = "http://www.welland.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 7):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
