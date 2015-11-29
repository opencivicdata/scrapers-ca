from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Vaughan(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519028'
    division_name = 'Vaughan'
    name = 'Vaughan City Council'
    url = 'https://www.vaughan.ca'
    use_type_id = True

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Vaughan', division_id=self.division_id)
        for seat_number in range(1, 4):
            organization.add_post(role='Regional Councillor', label='Vaughan (seat {})'.format(seat_number), division_id=self.division_id)
        for i in range(1, 6):
            organization.add_post(role='Councillor', label='Ward {}'.format(i))

        yield organization
