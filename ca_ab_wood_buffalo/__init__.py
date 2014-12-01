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

        organization.add_post(role='Mayor', label='Wood Buffalo')
        for i in range(6):
            organization.add_post(role='Councillor', label='Ward 1 (seat %d)' % (i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 2 (seat %d)' % (i + 1))
        organization.add_post(role='Councillor', label='Ward 3')
        organization.add_post(role='Councillor', label='Ward 4')

        yield organization
