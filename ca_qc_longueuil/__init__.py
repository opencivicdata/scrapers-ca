from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Longueuil(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:2458227"
    division_name = "Longueuil"
    name = "Conseil municipal de Longueuil"
    url = "http://www.longueuil.ca"
    exclude_types = ["borough"]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Maire", label=self.division_name, division_id=self.division_id)
        for division in Division.get(self.division_id).children("district"):
            if division.name == "Greenfield Park":
                for seat_number in range(1, 4):
                    organization.add_post(
                        role="Conseiller",
                        label=f"{division.name} (siège {seat_number})",
                        division_id=division.id,
                    )
            else:
                organization.add_post(role="Conseiller", label=division.name, division_id=division.id)

        yield organization
