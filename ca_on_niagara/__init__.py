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

        organization.add_post(role='Regional Chair', label='Niagara')

        counts = {
            'Fort Erie': 1,
            'Grimsby': 1,
            'Lincoln': 1,
            'Niagara Falls': 3,
            'Niagara-on-the-Lake': 1,
            'Pelham': 1,
            'Port Colborne': 1,
            'St. Catharines': 6,
            'Thorold': 1,  # can be 0
            'Wainfleet': 0,  # can be 1
            'Welland': 2,
            'West Lincoln': 0,
        }
        for label, count in counts.items():
            organization.add_post(role='Mayor', label=label)
            for i in range(count):
                organization.add_post(role='Councillor', label='%s (seat %d)' % (label, i + 1))

        yield organization
