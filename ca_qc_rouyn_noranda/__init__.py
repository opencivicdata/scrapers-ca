from pupa.scrape import Organization

from utils import CanadianJurisdiction


class RouynNoranda(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2486042"
    division_name = "Rouyn-Noranda"
    name = "Conseil municipal de Rouyn-Noranda"
    url = "https://www.rouyn-noranda.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Rouyn-Noranda", division_id=self.division_id)
        for i in range(1, 13):
            organization.add_post(role="Councillor", label=f"District {i}", division_id=self.division_id)
        yield organization
