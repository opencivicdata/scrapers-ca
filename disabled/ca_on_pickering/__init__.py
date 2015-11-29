from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Pickering(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518001'
    division_name = 'Pickering'
    name = 'Pickering City Council'
    url = 'http://www.pickering.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Pickering', division_id=self.division_id)
        for i in range(1, 4):
            organization.add_post(role='Regional Councillor', label='Ward {}'.format(i))
            organization.add_post(role='Councillor', label='Ward {}'.format(i))

        yield organization
