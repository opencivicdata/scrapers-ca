from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Peel(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3521'
    division_name = 'Peel'
    name = 'Peel Regional Council'
    url = 'http://www.peelregion.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Regional Chair', label='Peel')
        organization.add_post(role='Mayor', label='Caledon')
        organization.add_post(role='Mayor', label='Brampton')
        organization.add_post(role='Mayor', label='Mississauga')
        for i in range(5):
            organization.add_post(role='Councillor', label='Caledon Ward %d' % (i + 1))
        for i in range(10):
            organization.add_post(role='Councillor', label='Brampton Ward %d' % (i + 1))
        for i in range(11):
            organization.add_post(role='Councillor', label='Mississauga Ward %d' % (i + 1))

        yield organization
