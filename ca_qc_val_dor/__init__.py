from pupa.scrape import Organization

from utils import CanadianJurisdiction


class ValDor(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2489008"
    division_name = "Val-d'Or"
    name = "Conseil municipal de Val-d'Or"
    url = "https://ville.valdor.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for district_number in range(1, 9):
            organization.add_post(
                role="Conseiller",
                label=f"District {district_number}",
                division_id=f"{self.division_id}/district:{district_number}",
            )
        yield organization
