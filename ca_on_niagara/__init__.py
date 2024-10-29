from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Niagara(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/cd:3526"
    division_name = "Niagara"
    name = "Niagara Regional Council"
    url = "http://www.niagararegion.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Regional Chair", label=self.division_name, division_id=self.division_id)

        divisions = {
            "Fort Erie": {
                "count": 2,
                "type_id": "3526003",
            },
            "Grimsby": {
                "count": 2,
                "type_id": "3526065",
            },
            "Lincoln": {
                "count": 2,
                "type_id": "3526057",
            },
            "Niagara Falls": {
                "count": 4,
                "type_id": "3526043",
            },
            "Niagara-on-the-Lake": {
                "count": 2,
                "type_id": "3526047",
            },
            "Pelham": {
                "count": 2,
                "type_id": "3526028",
            },
            "Port Colborne": {
                "count": 2,
                "type_id": "3526011",
            },
            "St. Catharines": {
                "count": 8,
                "type_id": "3526053",
            },
            "Thorold": {
                "count": 2,
                "type_id": "3526037",
            },
            "Wainfleet": {
                "count": 1,
                "type_id": "3526014",
            },
            "Welland": {
                "count": 3,
                "type_id": "3526032",
            },
            "West Lincoln": {
                "count": 2,
                "type_id": "3526021",
            },
        }
        for division_name, division in divisions.items():
            division_id = "ocd-division/country:ca/csd:{}".format(division["type_id"])
            organization.add_post(role="Mayor", label=division_name, division_id=division_id)
            for seat_number in range(1, division["count"] + 1):
                organization.add_post(
                    role="Councillor", label=f"{division_name} (seat {seat_number})", division_id=division_id
                )

        yield organization
