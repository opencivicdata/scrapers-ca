from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Waterloo(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3530016'
    division_name = 'Waterloo'
    name = 'Waterloo City Council'
    url = 'http://www.waterloo.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Waterloo')
        for i in range(7):
            organization.add_post(role='Councillor', label='Ward {}'.format(i + 1))

        yield organization
