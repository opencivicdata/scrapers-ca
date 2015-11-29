from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Vancouver(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:5915022'
    division_name = 'Vancouver'
    name = 'Vancouver City Council'
    url = 'http://vancouver.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Vancouver', division_id=self.division_id)
        for seat_number in range(1, 11):
            organization.add_post(role='Councillor', label='Vancouver (seat {})'.format(seat_number), division_id=self.division_id)
        for seat_number in range(1, 8):
            organization.add_post(role='Commissioner', label='Vancouver (seat {})'.format(seat_number), division_id=self.division_id)

        yield organization
