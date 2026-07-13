from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Mirabel(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2474005"
    division_name = "Mirabel"
    name = "Conseil municipal de Mirabel"
    url = "https://mirabel.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mairesse", label=self.division_name, division_id=self.division_id)
        for district_number in range(1, 11):
            organization.add_post(
                role="Conseiller",
                label=f"District {district_number}",
                division_id=self.division_id,
            )

        yield organization
