from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SainteJulie(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2459010"
    division_name = "Sainte-Julie"
    name = "Conseil municipal de Sainte-Julie"
    url = "https://saintejulie.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for district_number in range(1, 9):
            organization.add_post(
                role="Conseiller",
                label=f"District {district_number}",
                division_id=self.division_id,
            )
        yield organization
