from pupa.scrape import Organization

from utils import CanadianJurisdiction


class GrandePrairieCountyNo1(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4819006"
    division_name = "Grande Prairie County No. 1"
    name = "County of Grande Prairie No. 1 Council"
    url = "http://www.countygp.ab.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division_number in range(1, 10):
            organization.add_post(
                role="Councillor",
                label=f"Division {division_number}",
                division_id=f"{self.division_id}/division:{division_number}",
            )

        yield organization
