from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class King(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519049'
    division_name = 'King'
    name = 'King Township Council'
    url = 'http://www.king.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 7):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id=self.division_id)

        yield organization
