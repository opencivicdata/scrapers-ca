from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SaintEustache(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2472005"
    division_name = "Saint-Eustache"
    name = "Conseil municipal de Saint-Eustache"
    url = "https://www.saint-eustache.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Saint-Eustache", division_id=self.division_id)
        for i in range(1, 11):
            organization.add_post(role="Councillor", label=f"District {i}", division_id=self.division_id)
        yield organization
