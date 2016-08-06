from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class ThunderBay(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3558004'
    division_name = 'Thunder Bay'
    name = 'Thunder Bay City Council'
    url = 'http://www.thunderbay.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 6):
            organization.add_post(role='Councillor at Large', label='Thunder Bay (seat {})'.format(seat_number), division_id=self.division_id)
        organization.add_post(role='Councillor', label='Current River')
        organization.add_post(role='Councillor', label='Red River')
        organization.add_post(role='Councillor', label='McKellar')
        organization.add_post(role='Councillor', label='McIntyre')
        organization.add_post(role='Councillor', label='Northwood')
        organization.add_post(role='Councillor', label='Westfort')
        organization.add_post(role='Councillor', label='Neebing')

        yield organization
