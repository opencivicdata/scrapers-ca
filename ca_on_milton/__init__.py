from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Milton(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3524009'
    division_name = 'Milton'
    name = 'Milton Town Council'
    url = 'http://www.milton.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 5):
            division_id = '{}/ward:{}'.format(self.division_id, ward_number)
            organization.add_post(role='Regional Councillor', label='Ward {}'.format(ward_number), division_id=division_id)
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id=division_id)

        yield organization
