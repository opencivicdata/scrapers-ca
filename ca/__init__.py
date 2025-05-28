from datetime import datetime

from opencivicdata.divisions import Division
from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Canada(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Parliament of Canada"
    url = "http://www.parl.gc.ca"
    parties = [
        {"name": "Bloc Québécois"},
        {"name": "Co-operative Commonwealth Federation"},
        {"name": "Conservative"},
        {"name": "Conservative Independent"},
        {"name": "Forces et Démocratie"},
        {"name": "Green Party"},
        {"name": "Groupe parlementaire québécois"},
        {"name": "Independent"},
        {"name": "Liberal"},
        {"name": "NDP"},
        {"name": "People's Party"},
        {"name": "Québec debout"},
    ]

    def get_organizations(self):
        parliament = Organization(self.name, classification=self.classification)
        yield parliament

        upper = Organization("Senate", classification="upper", parent_id=parliament)
        lower = Organization("House of Commons", classification="lower", parent_id=parliament)

        for division in Division.get(self.division_id).children("ed"):
            valid_from = division.attrs.get("validFrom")
            valid_through = getattr(division, "valid_through", None)
            if not valid_from:
                continue
            if valid_through and valid_through < datetime.now().strftime("%Y-%m-%d"):
                continue
            if valid_from > datetime.now().strftime("%Y-%m-%d"):
                continue
            lower.add_post(role="MP", label=division.name, division_id=division.id)

        # for ocd_type in ("province", "territory"):
        #     for province_or_territory in Division.get(self.division_id).children(ocd_type):
        #         for division in province_or_territory.children("fed"):
        #             valid_from = division.attrs.get("validFrom")
        #             valid_through = getattr(child, "valid_through", None)
        #             if valid_from and valid_from > datetime.now().strftime("%Y-%m-%d"):
        #                 continue
        #             if valid_through and valid_through < datetime.now().strftime("%Y-%m-%d"):
        #                 continue
        #             lower.add_post(role="MP", label=division.name, division_id=division.id)

        yield upper
        yield lower
