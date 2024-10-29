from opencivicdata.divisions import Division
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

        for division in Division.get(self.division_id).children("borough"):
            organization.add_post(role="Président", label=division.name, division_id=division.id)

        for division in Division.get(self.division_id).children("district"):
            organization.add_post(role="Conseiller", label=division.name, division_id=division.id)

        yield organization
