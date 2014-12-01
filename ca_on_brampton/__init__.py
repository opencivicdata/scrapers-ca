from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Brampton(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3521010'
    division_name = 'Brampton'
    name = 'Brampton City Council'
    url = 'http://www.brampton.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Brampton')
        organization.add_post(label='Wards 1 and 5', role='Regional Councillor')
        organization.add_post(label='Wards 1 and 5', role='Councillor')
        organization.add_post(label='Wards 2 and 6', role='Regional Councillor')
        organization.add_post(label='Wards 2 and 6', role='Councillor')
        organization.add_post(label='Wards 3 and 4', role='Regional Councillor')
        organization.add_post(label='Wards 3 and 4', role='Councillor')
        organization.add_post(label='Wards 7 and 8 (seat 1)', role='Regional Councillor')
        organization.add_post(label='Wards 7 and 8 (seat 2)', role='Regional Councillor')
        organization.add_post(label='Wards 9 and 10', role='Regional Councillor')
        organization.add_post(label='Wards 9 and 10', role='Councillor')

        yield organization
