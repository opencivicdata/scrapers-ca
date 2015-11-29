from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Cambridge(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3530010'
    division_name = 'Cambridge'
    name = 'Cambridge City Council'
    url = 'http://www.cambridge.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Cambridge', division_id=self.division_id)
        for i in range(2):
            organization.add_post(role='Regional Councillor', label='Cambridge (seat {})'.format(i + 1), division_id=self.division_id)
        for i in range(8):
            organization.add_post(role='Councillor', label='Ward {}'.format(i + 1))

        yield organization
