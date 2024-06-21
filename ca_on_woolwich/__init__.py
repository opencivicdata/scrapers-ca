from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Woolwich(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3530035"
    division_name = "Woolwich"
    name = "Woolwich Township Council"
    url = "http://www.woolwich.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        # Dictionary of ward number to stop index for seats
        stop = {
            1: 3,
            2: 2,
            3: 3,
        }
        for ward_number in range(1, 4):
            for seat_number in range(1, stop[ward_number]):
                organization.add_post(
                    role="Councillor",
                    label="Ward {} (seat {})".format(ward_number, seat_number),
                    division_id="{}/ward:{}".format(self.division_id, ward_number),
                )

        yield organization
