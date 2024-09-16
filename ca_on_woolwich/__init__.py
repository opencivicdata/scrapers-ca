from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Woolwich(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3530035"
    division_name = "Woolwich"
    name = "Woolwich Township Council"
    url = "http://www.woolwich.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number, stop in enumerate((3, 2, 3), 1):
            for seat_number in range(1, stop):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
