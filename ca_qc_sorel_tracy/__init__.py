from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SorelTracy(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2453052"
    division_name = "Sorel-Tracy"
    name = "Conseil municipal de Sorel-Tracy"
    url = "https://www.ville.sorel-tracy.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Sorel-Tracy", division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"District {i}", division_id=self.division_id)
        yield organization
