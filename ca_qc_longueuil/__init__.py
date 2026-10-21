from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Longueuil(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2458227"
    division_name = "Longueuil"
    name = "Conseil municipal de Longueuil"
    url = "http://www.longueuil.ca"
    exclude_types = ["borough", "district"]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        districts = [
            "Fatima-Parcours-du-Cerf",
            "LeMoyne-Jacques-Cartier",
            "Boisé-Du Tremblay",
            "Boisé-Fonrouge",
            "Saint-Charles",
            "Antoinette-Robidoux",
            "Georges-Dor",
            "Longueuil-Montréal-Sud",
            "Coteau-Rouge",
            "Croydon-Iberville",
            "Maraîchers",
            "Vieux-Saint-Hubert-la Savane",
            "Boisé-Pilon",
            "Parc-de-la-Cité",
            "Laflèche",
            "Ruisseau-Massé",
            "Greenfield Park (siège 1)",
            "Greenfield Park (siège 2)",
            "Greenfield Park (siège 3)",
        ]
        for district in districts:
            organization.add_post(role="Conseiller", label=district, division_id=self.division_id)

        yield organization
