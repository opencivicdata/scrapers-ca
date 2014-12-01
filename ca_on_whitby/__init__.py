from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Whitby(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518009'
    division_name = 'Whitby'
    name = 'Whitby Town Council'
    url = 'http://www.whitby.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Whitby')
        for i in range(3):
            organization.add_post(role='Regional Councillor', label='Durham (seat %d)' % (i + 1))
        organization.add_post(role='Councillor', label='North Ward')
        organization.add_post(role='Councillor', label='West Ward')
        organization.add_post(role='Councillor', label='Centre Ward')
        organization.add_post(role='Councillor', label='East Ward')

        yield organization
