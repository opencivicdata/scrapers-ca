from __future__ import unicode_literals
from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Saskatoon(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:4711066'
    division_name = 'Saskatoon'
    name = 'Saskatoon City Council'
    url = 'http://www.saskatoon.ca'
    use_type_id = True

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 11):
            organization.add_post(role='Councillor', label='Ward {}'.format(ward_number), division_id='{}/ward:{}'.format(self.division_id, ward_number))

        yield organization
