from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Caledon(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3521024"
    division_name = "Caledon"
    name = "Caledon Town Council"
    url = "https://www.caledon.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_name in ("Ward 1", "Ward 2", "Ward 3", "Ward 4", "Ward 5", "Ward 6"):
            organization.add_post(role="Regional Councillor", label=ward_name, division_id=self.division_id)
            organization.add_post(role="Councillor", label=ward_name, division_id=self.division_id)

        yield organization
