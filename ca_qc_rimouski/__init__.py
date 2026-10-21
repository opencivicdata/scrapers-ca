from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Rimouski(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2410043"
    division_name = "Rimouski"
    name = "Conseil municipal de Rimouski"
    url = "https://rimouski.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 12):
            organization.add_post(
                role="Councillor",
                label=f"District {i}",
                division_id=self.division_id,
            )

        yield organization
