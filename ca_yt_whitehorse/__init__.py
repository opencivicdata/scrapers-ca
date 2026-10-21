from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Whitehorse(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:6001009"
    division_name = "Whitehorse"
    name = "Whitehorse City Council"
    url = "https://www.whitehorse.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Whitehorse (seat {i})", division_id=self.division_id)
        yield organization
