from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Brantford(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3529006'
    division_name = 'Brantford'
    name = 'Brantford City Council'
    url = 'http://www.brantford.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Brantford', division_id=self.division_id)
        for ward_number in range(1, 6):
            organization.add_post(role='Councillor', label='Ward {} (seat 1)'.format(ward_number))
            organization.add_post(role='Councillor', label='Ward {} (seat 2)'.format(ward_number))

        yield organization
