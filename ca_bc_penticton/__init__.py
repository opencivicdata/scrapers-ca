from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Penticton(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5907041"
    division_name = "Penticton"
    name = "Penticton City Council"
    url = "https://www.penticton.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Penticton", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Penticton (seat {i})", division_id=self.division_id)
        yield organization
