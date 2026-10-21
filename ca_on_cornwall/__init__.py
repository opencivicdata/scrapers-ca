from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Cornwall(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3501012"
    division_name = "Cornwall"
    name = "Cornwall City Council"
    url = "https://www.cornwall.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 11):
            organization.add_post(
                role="Councillor",
                label=f"Councillor (seat {i})",
                division_id=self.division_id,
            )

        yield organization
