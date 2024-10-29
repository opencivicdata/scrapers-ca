from pupa.scrape import Organization

from utils import CanadianJurisdiction


class LaSalle(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3537034"
    division_name = "LaSalle"
    name = "LaSalle Town Council"
    url = "http://www.town.lasalle.on.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Deputy Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 6):
            organization.add_post(
                role="Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )

        yield organization
