from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Huron(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3540'
    division_name = 'Huron'
    name = 'Huron County Council'
    url = 'https://www.huroncounty.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        divisions = {
            'Ashfield-Colborne-Wawanosh': {
                'stop': 2,
                'type_id': '3540063',
            },
            'Bluewater': {
                'stop': 2,
                'type_id': '3540010',
            },
            'Central Huron': {
                'stop': 2,
                'type_id': '3540025',
            },
            'Goderich': {
                'stop': 2,
                'type_id': '3540028',
            },
            'Howick': {
                'stop': 1,
                'type_id': '3540046',
            },
            'Huron East': {
                'stop': 2,
                'type_id': '3540040',
            },
            'Morris-Turnberry': {
                'stop': 1,
                'type_id': '3540050',
            },
            'North Huron': {
                'stop': 1,
                'type_id': '3540055',
            },
            'South Huron': {
                'stop': 2,
                'type_id': '3540005',
            },
        }
        for division_name, division in divisions.items():
            division_id = 'ocd-division/country:ca/csd:{}'.format(division['type_id'])
            organization.add_post(role='Mayor', label=division_name, division_id=division_id)
            for seat_number in range(1, division['stop']):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(division_name, seat_number), division_id=division_id)

        yield organization
