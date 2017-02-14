from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Ajax(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3518005'
    division_name = 'Ajax'
    name = 'Ajax Town Council'
    url = 'http://www.ajax.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        organization.add_post(role='Regional Councillor', label='Wards 1 and 2')  # no single division_id
        organization.add_post(role='Regional Councillor', label='Wards 3 and 4')  # no single division_id
        for ward_number in range(1, 5):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
