from utils import CanadianJurisdiction
from pupa.scrape import Organization
from opencivicdata.divisions import Division
from datetime import datetime

class CanadaCandidates(CanadianJurisdiction):
    classification = "executive"
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Parliament of Canada"
    url = "http://www.parl.gc.ca"
    parties = [{"name": "Liberal Party"}, {"name": "Conservative Party"}, {"name": "Bloc Québécois"}, {"name": "New Democratic Party"}, {"name": "Green Party"}, {"name": "Independent"}]

    def get_organizations(self):
        parliament = Organization(self.name, classification=self.classification)
        yield parliament

        upper = Organization("Senate", classification="upper", parent_id=parliament)
        lower = Organization("House of Commons", classification="lower", parent_id=parliament)

        for division in Division.get(self.division_id).children("ed"):
            valid_from = division.attrs.get("validFrom")
            if valid_from and valid_from <= datetime.now().strftime("%Y-%m-%d") and valid_from < "2024-04-23":
                lower.add_post(role="MP", label=division.name, division_id=division.id)

        yield upper
        yield lower

