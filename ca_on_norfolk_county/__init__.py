from pupa.scrape import Organization

from utils import CanadianJurisdiction


class NorfolkCounty(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3528052"
    division_name = "Norfolk County"
    name = "Norfolk County Council"
    url = "https://www.norfolkcounty.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 5):
            organization.add_post(
                role="Councillor",
                label=f"Ward {ward_number}",
                division_id=f"{self.division_id}/ward:{ward_number}",
            )
        for seat_number in range(1, 3):
            organization.add_post(
                role="Councillor",
                label=f"Ward 5 (seat {seat_number})",
                division_id=f"{self.division_id}/ward:5",
            )
        for ward_number in range(6, 8):
            organization.add_post(
                role="Councillor",
                label=f"Ward {ward_number}",
                division_id=f"{self.division_id}/ward:{ward_number}",
            )

        yield organization
