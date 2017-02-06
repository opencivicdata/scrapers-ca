from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Peterborough(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3515014'
    division_name = 'Peterborough'
    name = 'Peterborough City Council'
    url = 'http://www.city.peterborough.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_name in ('Ashburnham', 'Monaghan', 'Northcrest', 'Otonabee', 'Town'):
            for seat_number in range(1, 9):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(ward_name, seat_number), division_id=self.division_id)

        yield organization
