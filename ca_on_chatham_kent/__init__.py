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

        organization.add_post(role='Mayor', label='Chatham-Kent')
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 1 (seat {})'.format(i + 1))
        for i in range(3):
            organization.add_post(role='Councillor', label='Ward 2 (seat {})'.format(i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 3 (seat {})'.format(i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 4 (seat {})'.format(i + 1))
        for i in range(2):
            organization.add_post(role='Councillor', label='Ward 5 (seat {})'.format(i + 1))
        for i in range(6):
            organization.add_post(role='Councillor', label='Ward 6 (seat {})'.format(i + 1))

        yield organization
