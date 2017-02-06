from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Caledon(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3521024'
    division_name = 'Caledon'
    name = 'Caledon Town Council'
    url = 'http://www.town.caledon.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_name in ('Ward 1', 'Ward 2', 'Wards 3 and 4', 'Ward 5'):
            for seat_number in range(1, 3):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(ward_name, seat_number), division_id=self.division_id)

        yield organization
