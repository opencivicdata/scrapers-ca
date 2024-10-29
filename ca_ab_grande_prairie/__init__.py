from pupa.scrape import Organization

from utils import CanadianJurisdiction


class GrandePrairie(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4819012"
    division_name = "Grande Prairie"
    name = "Grande Prairie City Council"
    url = "http://www.cityofgp.com"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 9):
            organization.add_post(
                role="Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )

        yield organization
