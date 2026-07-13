from pupa.scrape import Organization

from utils import CanadianJurisdiction


class StThomas(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3534021"
    division_name = "St. Thomas"
    name = "St. Thomas City Council"
    url = "https://www.stthomas.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="St. Thomas", division_id=self.division_id)
        for i in range(1, 9):
            organization.add_post(role="Councillor", label=f"St. Thomas (seat {i})", division_id=self.division_id)
        yield organization
