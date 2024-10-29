from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Oshawa(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3518013"
    division_name = "Oshawa"
    name = "Oshawa City Council"
    url = "http://www.oshawa.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 6):
            division_id = f"{self.division_id}/ward:{ward_number}"
            organization.add_post(role="Regional Councillor", label=f"Ward {ward_number}", division_id=division_id)
            organization.add_post(role="Councillor", label=f"Ward {ward_number}", division_id=division_id)

        yield organization
