from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Oshawa(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518013'
    division_name = 'Oshawa'
    name = 'Oshawa City Council'
    url = 'http://www.oshawa.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Oshawa')
        for i in range(7):
            organization.add_post(role='Regional Councillor', label='Oshawa (seat {})'.format(i + 1))
        for i in range(3):
            organization.add_post(role='Councillor', label='Oshawa (seat {})'.format(i + 1))

        yield organization
