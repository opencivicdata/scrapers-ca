from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class NewBrunswick(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:nb"
    division_name = "New Brunswick"
    name = "Legislative Assembly of New Brunswick"
    url = "https://www.legnb.ca/"
    parties = [
        {"name": "Green Party"},
        {"name": "Independent"},
        {"name": "Liberal Party"},
        {"name": "Progressive Conservative Party"},
    ]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division in Division.get(self.division_id).children("ed"):
            if division.id.split(":")[3].isdigit():
                organization.add_post(role="MLA", label=division.name, division_id=division.id)

        yield organization
