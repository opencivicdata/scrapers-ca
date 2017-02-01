from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Surrey(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:5915004'
    division_name = 'Surrey'
    name = 'Surrey City Council'
    url = 'http://www.surrey.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 9):
            organization.add_post(role='Councillor', label='Surrey (seat {})'.format(seat_number), division_id=self.division_id)

        yield organization
