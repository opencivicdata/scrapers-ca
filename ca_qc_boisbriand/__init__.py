from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Boisbriand(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2473005"
    division_name = "Boisbriand"
    name = "Conseil municipal de Boisbriand"
    url = "https://www.ville.boisbriand.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mairesse", label=self.division_name, division_id=self.division_id)
        for district in range(1, 9):
            organization.add_post(role="Conseiller", label=f"District {district}", division_id=self.division_id)
        yield organization
