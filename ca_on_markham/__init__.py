from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Markham(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519036'
    division_name = 'Markham'
    name = 'Markham City Council'
    url = 'http://www.markham.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Markham')
        organization.add_post(role='Deputy Mayor', label='Markham')
        for i in range(3):
            organization.add_post(role='Regional Councillor', label='York (seat %d)' % (i + 1))
        for i in range(8):
            organization.add_post(role='Councillor', label='Ward %d' % (i + 1))

        yield organization
