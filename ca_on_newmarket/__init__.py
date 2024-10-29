from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Newmarket(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3519048"
    division_name = "Newmarket"
    name = "Newmarket Town Council"
    url = "http://www.town.newmarket.on.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Deputy Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 8):
            organization.add_post(
                role="Councillor",
                label=f"Ward {ward_number}",
                division_id=f"{self.division_id}/ward:{ward_number}",
            )

        yield organization
