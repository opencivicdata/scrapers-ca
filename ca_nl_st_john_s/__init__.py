from pupa.scrape import Organization

from utils import CanadianJurisdiction


class StJohns(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:1001519"
    division_name = "St. John's"
    name = "St. John's City Council"
    url = "http://www.stjohns.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Deputy Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 5):
            organization.add_post(
                role="Councillor at Large",
                label=f"St. John's (seat {seat_number})",
                division_id=self.division_id,
            )
        for ward_number in range(1, 6):
            organization.add_post(
                role="Councillor",
                label=f"Ward {ward_number}",
                division_id=f"{self.division_id}/ward:{ward_number}",
            )

        yield organization
