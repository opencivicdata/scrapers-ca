from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SalaberryDeValleyfield(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2470052"
    division_name = "Salaberry-de-Valleyfield"
    name = "Conseil municipal de Salaberry-de-Valleyfield"
    url = "https://ville.valleyfield.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Salaberry-de-Valleyfield", division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"District {i}", division_id=self.division_id)
        yield organization
