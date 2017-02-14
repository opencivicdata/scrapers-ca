from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Cambridge(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3530010'
    division_name = 'Cambridge'
    name = 'Cambridge City Council'
    url = 'http://www.cambridge.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 3):
            organization.add_post(role='Regional Councillor', label='Cambridge (seat {})'.format(seat_number), division_id=self.division_id)
        for ward_number in range(1, 9):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
