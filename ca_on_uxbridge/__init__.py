from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Uxbridge(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518029'
    division_name = 'Uxbridge'
    name = 'Uxbridge Township Council'
    url = 'http://www.town.uxbridge.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        organization.add_post(role='Regional Councillor', label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 6):
            # @todo Until a boundary set is received and loaded into Represent, we treat this as having no divisions.
            # organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id=self.division_id)
            organization.add_post(role='Councillor', label='Uxbridge (seat {})'.format(ward_number), division_id=self.division_id)

        yield organization
