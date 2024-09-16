from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Clarington(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3518017"
    division_name = "Clarington"
    name = "Clarington Municipal Council"
    url = "http://www.clarington.net"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Regional Councillor", label="Wards 1 and 2")
        organization.add_post(role="Regional Councillor", label="Wards 3 and 4")
        for ward_number in range(1, 5):
            organization.add_post(role="Councillor", label=f"Ward {ward_number}")

        yield organization
