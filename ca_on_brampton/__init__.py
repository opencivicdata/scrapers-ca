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
        organization.add_post(role='Regional Councillor', label='Wards 1 and 5')
        organization.add_post(role='Councillor', label='Wards 1 and 5')
        organization.add_post(role='Regional Councillor', label='Wards 2 and 6')
        organization.add_post(role='Councillor', label='Wards 2 and 6')
        organization.add_post(role='Regional Councillor', label='Wards 3 and 4')
        organization.add_post(role='Councillor', label='Wards 3 and 4')
        organization.add_post(role='Regional Councillor', label='Wards 7 and 8 (seat 1)')
        organization.add_post(role='Regional Councillor', label='Wards 7 and 8 (seat 2)')
        organization.add_post(role='Regional Councillor', label='Wards 9 and 10')
        organization.add_post(role='Councillor', label='Wards 9 and 10')

        yield organization
