from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Lethbridge(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:4802012'
    division_name = 'Lethbridge'
    name = 'Lethbridge City Council'
    url = 'http://www.lethbridge.ca'

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Mayor', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 9):
            organization.add_post(role='Councillor', label='Lethbridge (seat {})'.format(seat_number), division_id=self.division_id)

        yield organization
