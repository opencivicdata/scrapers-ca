from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Peel(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3521'
    division_name = 'Peel'
    name = 'Peel Regional Council'
    url = 'http://www.peelregion.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Regional Chair', label='Peel')
        organization.add_post(role='Mayor', label='Caledon')
        organization.add_post(role='Mayor', label='Brampton')
        organization.add_post(role='Mayor', label='Mississauga')
        for i in range(1, 6):
            organization.add_post(role='Councillor', label='Caledon Ward {}'.format(i))
        for i in range(1, 11):
            organization.add_post(role='Councillor', label='Brampton Ward {}'.format(i))
        for i in range(1, 12):
            organization.add_post(role='Councillor', label='Mississauga Ward {}'.format(i))

        yield organization
