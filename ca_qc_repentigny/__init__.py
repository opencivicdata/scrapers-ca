from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Repentigny(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2460013"
    division_name = "Repentigny"
    name = "Conseil municipal de Repentigny"
    url = "https://repentigny.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        districts = [
            "District 1 - Repentigny-les-Bains",
            "District 2 - L'Hôtel-de-Ville",
            "District 3 - Centre-ville",
            "District 4 - Du Fleuve",
            "District 5 - Des Moulins",
            "District 6 - Félix-Leclerc",
            "District 7 - Valmont-sur-Parc",
            "District 8 - Jean-Baptiste-Meilleur",
            "District 9 - Du Boisé",
            "District 10 - Le Gardeur",
            "District 11 - Le Bourg-Neuf",
            "District 12 - Vieux-St-Paul",
        ]
        for district_number, district in enumerate(districts, start=1):
            organization.add_post(
                role="Conseiller",
                label=district,
                division_id=f"{self.division_id}/district:{district_number}",
            )

        yield organization
