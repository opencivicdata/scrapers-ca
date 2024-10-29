from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Vancouver(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5915022"
    division_name = "Vancouver"
    name = "Vancouver City Council"
    url = "http://vancouver.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 11):
            organization.add_post(
                role="Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )
        for seat_number in range(1, 8):
            organization.add_post(
                role="Commissioner",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )

        yield organization
