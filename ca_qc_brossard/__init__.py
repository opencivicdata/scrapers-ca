from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Brossard(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2458007"
    division_name = "Brossard"
    name = "Conseil municipal de Brossard"
    url = "http://www.ville.brossard.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for district_number in range(1, 13):
            organization.add_post(
                role="Conseiller",
                label=f"District {district_number}",
                division_id=self.division_id,
            )
        yield organization
