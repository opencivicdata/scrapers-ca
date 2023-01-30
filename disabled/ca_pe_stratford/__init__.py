from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Stratford(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:1102080"
    division_name = "Stratford"
    name = "Stratford Town Council"
    url = "http://www.townofstratford.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Councillor", label="Kelly's Cove (seat 1)")
        organization.add_post(role="Councillor", label="Kelly's Cove (seat 2)")
        organization.add_post(role="Councillor", label="Stewart Cove (seat 1)")
        organization.add_post(role="Councillor", label="Stewart Cove (seat 2)")
        organization.add_post(role="Councillor", label="Tea Hill (seat 1)")
        organization.add_post(role="Councillor", label="Tea Hill (seat 2)")

        yield organization
