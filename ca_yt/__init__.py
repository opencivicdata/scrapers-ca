from pupa.scrape import Organization

from utils import CanadianJurisdiction

RIDINGS = [
    "Porter Creek North",
    "Mayo-Tatchun",
    "Whistle Bend South",
    "Lake Laberge",
    "Whistle Bend North",
    "Copperbelt North",
    "Marsh Lake-Mount Lorne-Golden Horn",
    "Porter Creek South",
    "Riverdale North",
    "Kluane",
    "Copperbelt South",
    "Porter Creek Centre",
    "Whitehorse West",
    "Klondike",
    "Watson Lake-Ross River-Faro",
    "Mountainview",
    "Southern Lakes",
    "Vuntut Gwitchin",
    "Whitehorse Centre",
    "Takhini",
    "Riverdale South",
]


class Yukon(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/territory:yt"
    division_name = "Yukon"
    name = "Legislative Assembly of Yukon"
    url = "https://yukonassembly.ca"
    parties = [{"name": "Yukon Liberal Party"}, {"name": "Yukon Party"}, {"name": "New Democratic Party"}]

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        for riding in RIDINGS:
            organization.add_post(role="MLA", label=riding, division_id=self.division_id)
        yield organization
