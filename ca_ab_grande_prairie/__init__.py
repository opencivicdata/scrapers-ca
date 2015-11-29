from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class GrandePrairie(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:4819012'
    division_name = 'Grande Prairie'
    name = 'Grande Prairie City Council'
    url = 'http://www.cityofgp.com'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Grande Prairie', division_id=self.division_id)
        for i in range(8):
            organization.add_post(role='Councillor', label='Grande Prairie (seat {})'.format(i + 1), division_id=self.division_id)

        yield organization
