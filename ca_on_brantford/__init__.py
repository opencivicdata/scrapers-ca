from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Brantford(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3529006'
    division_name = 'Brantford'
    name = 'Brantford City Council'
    url = 'http://www.city.brantford.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Brantford')
        for i in range(5):
            organization.add_post(role='Councillor', label='Ward {} (seat 1)'.format(i + 1))
            organization.add_post(role='Councillor', label='Ward {} (seat 2)'.format(i + 1))

        yield organization
