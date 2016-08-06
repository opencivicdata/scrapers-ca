from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Grimsby(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3526065'
    division_name = 'Grimsby'
    name = 'Grimsby Town Council'
    url = 'http://www.grimsby.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 5):
            for seat_number in range(1, 3):
                organization.add_post(role='Alderman', label='Ward {} (seat {})'.format(ward_number, seat_number))

        yield organization
