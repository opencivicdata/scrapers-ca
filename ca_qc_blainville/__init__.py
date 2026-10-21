from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Blainville(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2473015"
    division_name = "Blainville"
    name = "Conseil municipal de Blainville"
    url = "https://blainville.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mairesse", label=self.division_name, division_id=self.division_id)
        districts = [
            "District Fontainebleau (no 1)",
            "District de la Côte-Saint-Louis (no 2)",
            "District Saint-Rédempteur (no 3)",
            "District du Plan-Bouchard (no 4)",
            "District Notre-Dame-de-l'Assomption (no 5)",
            "District Chante-Bois (no 6)",
            "District des Hirondelles (no 7)",
            "District d’Alençon (no 8)",
            "District de la Renaissance (no 9)",
            "District du Blainvillier (no 10)",
            "District du Coteau (no 11)",
            "District Henri-Dunant (no 12)",
        ]
        for district in districts:
            organization.add_post(
                role="Conseiller",
                label=district,
                division_id=self.division_id,
            )

        yield organization
