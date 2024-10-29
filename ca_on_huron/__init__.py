from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Huron(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/cd:3540"
    division_name = "Huron"
    name = "Huron County Council"
    url = "https://www.huroncounty.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        divisions = {
            "Ashfield-Colborne-Wawanosh": {
                "count": 2,
                "type_id": "3540063",
            },
            "Bluewater": {
                "count": 2,
                "type_id": "3540010",
            },
            "Central Huron": {
                "count": 2,
                "type_id": "3540025",
            },
            "Goderich": {
                "count": 2,
                "type_id": "3540028",
            },
            "Howick": {
                "count": 1,
                "type_id": "3540046",
            },
            "Huron East": {
                "count": 2,
                "type_id": "3540040",
            },
            "Morris-Turnberry": {
                "count": 1,
                "type_id": "3540050",
            },
            "North Huron": {
                "count": 1,
                "type_id": "3540055",
            },
            "South Huron": {
                "count": 2,
                "type_id": "3540005",
            },
        }
        for division_name, division in divisions.items():
            division_id = "ocd-division/country:ca/csd:{}".format(division["type_id"])
            for seat_number in range(1, division["count"] + 1):
                organization.add_post(
                    role="Councillor",
                    label=f"{division_name} (seat {seat_number})",
                    division_id=division_id,
                )

        yield organization
