from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Moncton(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:1307022'
    division_name = 'Moncton'
    name = 'Moncton City Council'
    url = 'http://www.moncton.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Moncton')
        for i in range(2):
            organization.add_post(role='Councillor at Large', label='Moncton (seat %d)' % (i + 1))
        for i in range(4):
          for j in range(2):
              organization.add_post(role='Councillor', label='Ward %d (seat %d)' % (i + 1, j + 1))

        yield organization
