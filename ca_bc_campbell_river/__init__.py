from pupa.scrape import Organization

from utils import CanadianJurisdiction


class CampbellRiver(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5924034"
    division_name = "Campbell River"
    name = "Campbell River City Council"
    url = "https://www.campbellriver.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Campbell River", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Campbell River (seat {i})", division_id=self.division_id)
        yield organization
