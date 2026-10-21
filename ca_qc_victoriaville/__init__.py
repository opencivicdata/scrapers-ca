from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Victoriaville(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2439062"
    division_name = "Victoriaville"
    name = "Conseil municipal de Victoriaville"
    url = "https://victoriaville.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 11):
            organization.add_post(
                role="Councillor",
                label=f"District {i}",
                division_id=self.division_id,
            )

        yield organization
