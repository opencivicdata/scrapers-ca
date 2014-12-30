from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Clarington(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518017'
    division_name = 'Clarington'
    name = 'Clarington Municipal Council'
    url = 'http://www.clarington.net'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Clarington')
        organization.add_post(role='Regional Councillor', label='Wards 1 and 2')
        organization.add_post(role='Regional Councillor', label='Wards 3 and 4')
        for i in range(4):
            organization.add_post(role='Councillor', label='Ward %d' % (i + 1))

        yield organization
