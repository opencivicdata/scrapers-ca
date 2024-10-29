from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Pickering(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3518001"
    division_name = "Pickering"
    name = "Pickering City Council"
    url = "http://www.pickering.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 4):
            organization.add_post(role="Regional Councillor", label=f"Ward {ward_number}")
            organization.add_post(role="Councillor", label=f"Ward {ward_number}")

        yield organization
