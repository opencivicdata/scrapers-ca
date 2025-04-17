# https://github.com/opencivicdata/scrapers-ca/blob/b19f84783efe046fac96426ebe6e1d7c8dcf1fcd/ca_candidates/__init__.py
import re

from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class CanadaCandidates(CanadianJurisdiction):
    classification = "executive"
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Parliament of Canada"
    url = "http://www.parl.gc.ca"
    parties = [
        {"name": "Liberal Party"},
        {"name": "Conservative Party"},
        {"name": "Bloc Québécois"},
        {"name": "New Democratic Party"},
        {"name": "Green Party"},
        {"name": "Independent"},
        {"name": "People's Party of Canada"},
        {"name": "Marxist-Leninist Party of Canada"},
        {"name": "Animal Protection Party of Canada"},
        {"name": "Centrist Party of Canada"},
        {"name": "Christian Heritage Party of Canada"},
        {"name": "United Party of Canada (UP)"},
        {"name": "Marijuana Party"},
        {"name": "Parti Rhinocéros Party"},
        {"name": "Libertarian Party of Canada"},
        {"name": "Communist Party of Canada"},
        {"name": "Canadian Future Party"},
    ]

    def get_organizations(self):
        parliament = Organization(self.name, classification=self.classification)
        yield parliament

        upper = Organization("Senate", classification="upper", parent_id=parliament)
        lower = Organization("House of Commons", classification="lower", parent_id=parliament)

        for division in Division.get(self.division_id).children("ed"):
            if "2023" in division.id:
                lower.add_post(role="candidate", label=division.name, division_id=division.id)
                lower.add_post(  # parties can't spell
                    role="candidate", label=re.search(r"(\d+)-2023\Z", division.id).group(1), division_id=division.id
                )

        yield upper
        yield lower
