from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Welland(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3526032'
    division_name = 'Welland'
    name = 'Welland City Council'
    url = 'http://www.welland.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Welland')
        for i in range(6):
            for j in range(2):
                organization.add_post(role='Councillor', label='Ward %d (seat %d)' % (i + 1, j + 1))

        yield organization
