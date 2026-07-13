from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SeptIles(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2497007"
    division_name = "Sept-Îles"
    name = "Conseil municipal de Sept-Îles"
    url = "https://www.septiles.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for district in range(1, 10):
            organization.add_post(role="Conseiller", label=f"District {district}", division_id=self.division_id)
        yield organization
