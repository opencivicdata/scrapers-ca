from pupa.scrape import Organization

from utils import CanadianJurisdiction


class WestKelowna(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5935029"
    division_name = "West Kelowna"
    name = "West Kelowna City Council"
    url = "https://www.westkelownacity.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="West Kelowna", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"West Kelowna (seat {i})", division_id=self.division_id)
        yield organization
