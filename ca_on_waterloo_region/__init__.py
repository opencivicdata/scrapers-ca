from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Waterloo(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3530'
    division_name = 'Waterloo'
    name = 'Waterloo Regional Council'
    url = 'http://www.regionofwaterloo.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Chair', label='Waterloo')
        organization.add_post(role='Regional Councillor', label='Cambridge')
        organization.add_post(role='Regional Councillor', label='Kitchener')
        organization.add_post(role='Regional Councillor', label='Waterloo')
        organization.add_post(role='Regional Councillor', label='North Dumfries')
        organization.add_post(role='Regional Councillor', label='Wellesley')
        organization.add_post(role='Regional Councillor', label='Wilmot')
        organization.add_post(role='Regional Councillor', label='Woolwich')
        for seat_number in range(1, 3):
            organization.add_post(role='Regional Councillor', label='Cambridge (seat {})'.format(seat_number))
        for seat_number in range(1, 5):
            organization.add_post(role='Regional Councillor', label='Kitchener (seat {})'.format(seat_number))
        for seat_number in range(1, 3):
            organization.add_post(role='Regional Councillor', label='Waterloo (seat {})'.format(seat_number))

        yield organization
