from pupa.scrape import Organization

from utils import CanadianJurisdiction


class VaudreuilDorion(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2471083"
    division_name = "Vaudreuil-Dorion"
    name = "Conseil municipal de Vaudreuil-Dorion"
    url = "https://ville.vaudreuil-dorion.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Vaudreuil-Dorion", division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"District {i}", division_id=self.division_id)
        yield organization
