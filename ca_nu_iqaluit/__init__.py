from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Iqaluit(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:6204003"
    division_name = "Iqaluit"
    name = "Iqaluit City Council"
    url = "https://iqaluit.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"Iqaluit (seat {i})", division_id=self.division_id)
        yield organization
