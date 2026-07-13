from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Levis(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2425213"
    division_name = "Lévis"
    name = "Conseil municipal de Lévis"
    url = "http://www.ville.levis.qc.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)

        for borough in (
            "Desjardins",
            "Les Chutes-de-la-Chaudière-Est",
            "Les Chutes-de-la-Chaudière-Ouest",
        ):
            organization.add_post(role="Président", label=borough, division_id=self.division_id)

        for district_number in range(1, 16):
            organization.add_post(
                role="Conseiller",
                label=f"District {district_number}",
                division_id=self.division_id,
            )

        yield organization
