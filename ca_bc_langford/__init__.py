from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Langford(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5917044"
    division_name = "Langford"
    name = "Langford City Council"
    url = "https://langford.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(
                role="Councillor",
                label=f"Langford (seat {i})",
                division_id=self.division_id,
            )

        yield organization
