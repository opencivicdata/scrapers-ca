from pupa.scrape import Organization

from utils import CanadianJurisdiction


class NiagaraOnTheLake(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3526047"
    division_name = "Niagara-on-the-Lake"
    name = "Niagara-on-the-Lake Town Council"
    url = "https://www.notl.org"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Lord Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Regional Councillor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 9):
            organization.add_post(
                role="Councillor",
                label=f"{self.division_name} (seat {seat_number})",
                division_id=self.division_id,
            )

        yield organization
