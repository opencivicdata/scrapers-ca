from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Dieppe(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:1307045"
    division_name = "Dieppe"
    name = "Dieppe City Council"
    url = "https://www.dieppe.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat in range(1, 4):
            organization.add_post(
                role="Councillor at Large", label=f"{self.division_name} (seat {seat})", division_id=self.division_id
            )
        for ward in range(1, 6):
            organization.add_post(role="Councillor", label=f"Ward {ward}", division_id=self.division_id)
        yield organization
