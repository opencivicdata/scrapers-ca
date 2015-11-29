from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class LaSalle(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3537034'
    division_name = 'LaSalle'
    name = 'LaSalle Town Council'
    url = 'http://www.town.lasalle.on.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='LaSalle', division_id=self.division_id)
        organization.add_post(role='Deputy Mayor', label='LaSalle', division_id=self.division_id)
        for i in range(5):
            organization.add_post(role='Councillor', label='LaSalle (seat {})'.format(i + 1), division_id=self.division_id)

        yield organization
