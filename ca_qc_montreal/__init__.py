from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Montreal(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2466023"
    division_name = "Montréal"
    name = "Conseil municipal de Montréal"
    url = "http://www.ville.montreal.qc.ca"
    parties = [
        {"name": "Coalition Montréal"},
        {"name": "Ensemble Montréal"},
        {"name": "Indépendant"},
        {"name": "Projet Montréal - Équipe Valérie Plante"},
        {"name": "Vrai changement pour Montréal"},
        {"name": "Équipe Anjou"},
        {"name": "Équipe LaSalle Team"},
        {"name": "Équipe Dauphin Lachine"},
        {"name": "Équipe Denis Coderre pour Montréal"},
    ]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(
            role="Maire de la Ville de Montréal", label=self.division_name, division_id=self.division_id
        )  # 0,00

        for division in Division.get(self.division_id).children("borough"):  # 18
            if (
                division.id != "ocd-division/country:ca/csd:2466023/borough:18"
            ):  # Maire de la Ville de Montréal is Maire d'arrondissement for Ville-Marie
                organization.add_post(role="Maire d'arrondissement", label=division.name, division_id=division.id)

        for division in Division.get(self.division_id).children("district"):  # 46
            borough_id = division.id.rsplit(":", 1)[1].split(".", 1)[0]
            if borough_id not in ("2", "4", "6", "9"):
                organization.add_post(role="Conseiller de la ville", label=division.name, division_id=division.id)

        organization.add_post(
            role="Conseiller de la ville", label="Anjou", division_id="ocd-division/country:ca/csd:2466023/borough:2"
        )
        organization.add_post(
            role="Conseiller de la ville", label="Lachine", division_id="ocd-division/country:ca/csd:2466023/borough:4"
        )

        yield organization
