from utils import CanadianJurisdiction
from pupa.scrape import Organization


class SaintJohn(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:1301006'
    division_name = 'Saint John'
    name = 'Saint John City Council'
    url = 'http://www.saintjohn.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        organization.add_post(role='Deputy Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='{} (seat {})'.format(self.division_name, seat_number), division_id=self.division_id)
        for ward_number in range(1, 5):
            for seat_number in range(1, 3):
                organization.add_post(role='Councillor', label='Ward {} (seat {})'.format(ward_number, seat_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
