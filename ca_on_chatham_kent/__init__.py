from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class ChathamKent(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3536020'
    division_name = 'Chatham-Kent'
    name = 'Chatham-Kent Municipal Council'
    url = 'http://www.chatham-kent.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='Ward 1 (seat {})'.format(seat_number))
        for seat_number in range(1, 4):
            organization.add_post(role='Councillor', label='Ward 2 (seat {})'.format(seat_number))
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='Ward 3 (seat {})'.format(seat_number))
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='Ward 4 (seat {})'.format(seat_number))
        for seat_number in range(1, 3):
            organization.add_post(role='Councillor', label='Ward 5 (seat {})'.format(seat_number))
        for seat_number in range(1, 7):
            organization.add_post(role='Councillor', label='Ward 6 (seat {})'.format(seat_number))

        yield organization
