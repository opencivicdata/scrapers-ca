from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Vancouver(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:5915022'
    division_name = 'Vancouver'
    name = 'Vancouver City Council'
    url = 'http://vancouver.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Vancouver')
        for i in range(10):
              organization.add_post(role='Councillor', label='Vancouver (seat %d)' % (i + 1))
        for i in range(7):
              organization.add_post(role='Commissioner', label='Vancouver (seat %d)' % (i + 1))

        yield organization
