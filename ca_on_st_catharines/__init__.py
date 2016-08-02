from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class StCatharines(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:3526053'
    division_name = 'St. Catharines'
    name = 'St. Catharines City Council'
    url = 'http://www.stcatharines.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label='St. Catharines', division_id=self.division_id)
        for ward_name in ('Grantham', 'Merritton', 'Port Dalhousie', "St. Andrew's", "St. George's", "St. Patrick's"):
            for seat_number in range(1, 3):
                organization.add_post(role='Councillor', label='{} (seat {})'.format(ward_name, seat_number))

        yield organization
