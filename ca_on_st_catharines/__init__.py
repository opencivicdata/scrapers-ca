from pupa.scrape import Organization

from utils import CanadianJurisdiction, clean_type_id


class StCatharines(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3526053"
    division_name = "St. Catharines"
    name = "St. Catharines City Council"
    url = "http://www.stcatharines.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_name in ("Grantham", "Merritton", "Port Dalhousie", "St. Andrew's", "St. George's", "St. Patrick's"):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"{ward_name} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{clean_type_id(ward_name)}",
                )

        yield organization
