from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class GrandePrairieCountyNo1(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:4819006'
    division_name = 'Grande Prairie County No. 1'
    name = 'County of Grande Prairie No. 1 Council'
    url = 'http://www.countygp.ab.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division_number in range(1, 10):
            # One of the councillors is the Reeve.
            if division_number == 3:
                role = 'Reeve'
            else:
                role = 'Councillor'
            organization.add_post(role=role, label='Division {}'.format(division_number), division_id='{}/division:{}'.format(self.division_id, division_number))

        yield organization
