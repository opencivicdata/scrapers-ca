from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Innisfil(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3543017"
    division_name = "Innisfil"
    name = "Innisfil Town Council"
    url = "https://www.innisfil.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Innisfil", division_id=self.division_id)
        organization.add_post(role="Councillor", label="Deputy Mayor", division_id=self.division_id)
        for i in range(1, 8):
            organization.add_post(role="Councillor", label=f"Ward {i}", division_id=self.division_id)
        yield organization
