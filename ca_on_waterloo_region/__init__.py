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
        organization.add_post(role='Councillor', label='Cambridge (mayor)')
        organization.add_post(role='Councillor', label='Kitchener (mayor)')
        organization.add_post(role='Councillor', label='Waterloo (mayor)')
        organization.add_post(role='Councillor', label='North Dumfries (mayor)')
        organization.add_post(role='Councillor', label='Wellesley (mayor)')
        organization.add_post(role='Councillor', label='Wilmot (mayor)')
        organization.add_post(role='Councillor', label='Woolwich (mayor)')
        for i in range(2):
            organization.add_post(role='Councillor', label='Cambridge (seat %d)' % (i + 1))
        for i in range(4):
            organization.add_post(role='Councillor', label='Kitchener (seat %d)' % (i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Waterloo (seat %d)' % (i + 1))

        yield organization
