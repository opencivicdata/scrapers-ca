from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Lambton(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/cd:3538'
    division_name = 'Lambton'
    name = 'Lambton County Council'
    url = 'http://www.lambtononline.ca'

    def get_organizations(self):  # @todo Fix labels along the lines of the regions of Peel, Niagara or Waterloo.
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role='Warden', label=self.division_name, division_id=self.division_id)
        organization.add_post(role='Deputy Warden', label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 16):
            organization.add_post(role='Councillor', label='Lambton (seat {})'.format(seat_number), division_id=self.division_id)

        yield organization
