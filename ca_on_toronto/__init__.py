from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Toronto(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3520005"
    division_name = "Toronto"
    name = "Toronto City Council"
    url = "http://www.toronto.ca"
    skip_null_valid_from = True

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for division in Division.get(self.division_id).children("ward"):
            if "2018" in division.id:
                organization.add_post(role="Councillor", label=division.name, division_id=division.id)

        yield organization
