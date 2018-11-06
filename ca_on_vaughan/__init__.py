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

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 4):
            organization.add_post(role='Regional Councillor', label='{} (seat {})'.format(self.division_name, seat_number), division_id=self.division_id)
        for ward_number in range(1, 6):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
