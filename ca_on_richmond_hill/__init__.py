from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class RichmondHill(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519038'
    division_name = 'Richmond Hill'
    name = 'Richmond Hill Town Council'
    url = 'http://www.town.richmond-hill.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Richmond Hill', division_id=self.division_id)
        for i in range(1, 3):
            organization.add_post(role='Regional Councillor', label='Richmond Hill (seat {})'.format(i), division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role='Councillor', label='Ward {}'.format(i))

        yield organization
