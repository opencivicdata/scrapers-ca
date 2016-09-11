from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class WoodBuffalo(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:4816037'
    division_name = 'Wood Buffalo'
    name = 'Wood Buffalo Municipal Council'
    url = 'http://www.woodbuffalo.ab.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 7):
            organization.add_post(role='Councillor', label='Ward 1 (seat {})'.format(seat_number), division_id='{}/ward:1'.format(self.division_id))
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='Ward 2 (seat {})'.format(seat_number), division_id='{}/ward:2'.format(self.division_id))
        organization.add_post(role='Councillor', label='Ward 3', division_id='{}/ward:3'.format(self.division_id))
        organization.add_post(role='Councillor', label='Ward 4', division_id='{}/ward:4'.format(self.division_id))

        yield organization
