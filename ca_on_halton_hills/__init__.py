from pupa.scrape import Organization

from utils import CanadianJurisdiction


class HaltonHills(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3524015"
    division_name = "Halton Hills"
    name = "Halton Hills Town Council"
    url = "https://www.haltonhills.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(
            role="Regional Councillor",
            label="Wards 1 and 2",
            division_id=self.division_id,
        )
        organization.add_post(
            role="Regional Councillor",
            label="Wards 3 and 4",
            division_id=self.division_id,
        )
        for ward_number in range(1, 5):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
