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

        organization.add_post(role='Mayor', label='Richmond Hill')
        for i in range(2):
            organization.add_post(role='Regional Councillor', label='Richmond Hill (seat {})'.format(i + 1))
        for i in range(6):
            organization.add_post(role='Councillor', label='Ward {}'.format(i + 1))

        yield organization
