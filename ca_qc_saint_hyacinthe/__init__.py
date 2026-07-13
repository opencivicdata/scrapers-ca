from pupa.scrape import Organization

from utils import CanadianJurisdiction


class SaintHyacinthe(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2454048"
    division_name = "Saint-Hyacinthe"
    name = "Conseil municipal de Saint-Hyacinthe"
    url = "https://www.st-hyacinthe.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        districts = [
            "District 1 - Sainte-Rosalie",
            "District 2 - Yamaska",
            "District 3 - Saint-Joseph",
            "District 4 - La Providence",
            "District 5 - Douville Sud",
            "District 6 - Saint-Thomas-d'Aquin",
            "District 7 - Saint-Sacrement-Sacré-Coeur",
            "District 8 - Bois-Joli",
            "District 9 - Douville Nord-Notre-Dame",
            "District 10 - Cascades",
        ]
        for district_number, district in enumerate(districts, start=1):
            organization.add_post(
                role="Conseiller",
                label=district,
                division_id=f"{self.division_id}/district:{district_number}",
            )

        yield organization
