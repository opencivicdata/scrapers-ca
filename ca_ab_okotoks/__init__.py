from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Okotoks(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4806012"
    division_name = "Okotoks"
    name = "Okotoks Town Council"
    url = "https://www.okotoks.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 7):
            organization.add_post(
                role="Councillor", label=f"Okotoks (seat {seat_number})", division_id=self.division_id
            )
        yield organization
