from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Oakville(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3524001'
    division_name = 'Oakville'
    name = 'Oakville Town Council'
    url = 'http://www.oakville.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Oakville')
        for i in range(6):
            organization.add_post(role='Regional Councillor', label='Ward %d' % (i + 1))
            organization.add_post(role='Councillor', label='Ward %d' % (i + 1))

        yield organization
