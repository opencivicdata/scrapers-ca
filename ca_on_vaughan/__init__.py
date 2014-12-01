from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Vaughan(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3519028'
    division_name = 'Vaughan'
    name = 'Vaughan City Council'
    url = 'https://www.vaughan.ca'
    use_type_id = True

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='Vaughan')
        for i in range(3):
            organization.add_post(role='Regional Councillor', label='York (seat %d)' % (i + 1))
        for i in range(5):
            organization.add_post(role='Councillor', label='Ward %d' % (i + 1))

        yield organization
