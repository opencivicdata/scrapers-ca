from pupa.scrape import Organization

from utils import CanadianJurisdiction


class ThetfordMines(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2431084"
    division_name = "Thetford Mines"
    name = "Conseil municipal de Thetford Mines"
    url = "https://www.villethetford.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for district in range(1, 9):
            organization.add_post(role="Conseiller", label=f"District {district}", division_id=self.division_id)
        yield organization
