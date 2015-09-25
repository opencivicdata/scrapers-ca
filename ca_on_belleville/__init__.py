from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Belleville(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3512005'
    division_name = 'Belleville'
    name = 'Belleville City Council'
    url = 'http://www.city.belleville.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Belleville')
        for i in range(6):
            organization.add_post(role='Councillor', label='Ward 1 (seat {})'.format(i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 2 (seat {})'.format(i + 1))

        yield organization
