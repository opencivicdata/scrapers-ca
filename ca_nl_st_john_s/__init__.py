from utils import CanadianJurisdiction
from pupa.scrape import Organization


class StJohns(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:1001519'
    division_name = "St. John's"
    name = "St. John's City Council"
    url = 'http://www.stjohns.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        organization.add_post(role='Deputy Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 5):
            organization.add_post(role='Councillor at Large', label="St. John's (seat {})".format(seat_number), division_id=self.division_id)
        for ward_number in range(1, 6):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
