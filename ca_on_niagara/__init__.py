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

        counts = {
            'Fort Erie': 2,
            'Grimsby': 2,
            'Lincoln': 2,
            'Niagara Falls': 4,
            'Niagara-on-the-Lake': 2,
            'Pelham': 2,
            'Port Colborne': 2,
            'St. Catharines': 7,
            'Thorold': 2,  # can be 1
            'Wainfleet': 1,  # can be 2
            'Welland': 3,
            'West Lincoln': 1,
        }
        for label, count in counts.items():
            organization.add_post(role='Mayor', label=label)
            for i in range(1, count):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(label, i))

        yield organization
