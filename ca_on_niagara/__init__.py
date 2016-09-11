from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Niagara(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3526'
    division_name = 'Niagara'
    name = 'Niagara Regional Council'
    url = 'http://www.niagararegion.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Regional Chair', label='Niagara', division_id=self.division_id)

        divisions = {
            'Fort Erie': {
                'stop': 3,
                'type_id': '3526003',
            },
            'Grimsby': {
                'stop': 3,
                'type_id': '3526065',
            },
            'Lincoln': {
                'stop': 3,
                'type_id': '3526057',
            },
            'Niagara Falls': {
                'stop': 5,
                'type_id': '3526043',
            },
            'Niagara-on-the-Lake': {
                'stop': 3,
                'type_id': '3526047',
            },
            'Pelham': {
                'stop': 3,
                'type_id': '3526028',
            },
            'Port Colborne': {
                'stop': 3,
                'type_id': '3526011',
            },
            'St. Catharines': {
                'stop': 8,
                'type_id': '3526053',
            },
            'Thorold': {
                'stop': 3,  # can be 2
                'type_id': '3526037',
            },
            'Wainfleet': {
                'stop': 2,  # can be 3
                'type_id': '3526014',
            },
            'Welland': {
                'stop': 4,
                'type_id': '3526032',
            },
            'West Lincoln': {
                'stop': 2,
                'type_id': '3526021',
            },
        }
        for division_name, division in divisions.items():
            division_id = 'ocd-division/country:ca/csd:{}'.format(division['type_id'])
            organization.add_post(role='Mayor', label=division_name, division_id=division_id)
            for seat_number in range(1, division['stop']):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(division_name, seat_number), division_id=division_id)

        yield organization
