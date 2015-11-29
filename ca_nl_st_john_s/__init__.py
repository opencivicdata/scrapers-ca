from __future__ import unicode_literals
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

        organization.add_post(role='Mayor', label="St. John's", division_id=self.division_id)
        organization.add_post(role='Deputy Mayor', label="St. John's", division_id=self.division_id)
        for i in range(1, 5):
            organization.add_post(role='Councillor at Large', label="St. John's (seat {})".format(i), division_id=self.division_id)
        for i in range(1, 6):
            organization.add_post(role='Councillor', label='Ward {}'.format(i))

        yield organization
