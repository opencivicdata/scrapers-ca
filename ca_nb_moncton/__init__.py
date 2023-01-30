from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Moncton(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:1307022"
    division_name = "Moncton"
    name = "Moncton City Council"
    url = "http://www.moncton.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for seat_number in range(1, 3):
            organization.add_post(
                role="Councillor at Large",
                label="{} (seat {})".format(self.division_name, seat_number),
                division_id=self.division_id,
            )
        for ward_number in range(1, 5):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label="Ward {} (seat {})".format(ward_number, seat_number),
                    division_id="{}/ward:{}".format(self.division_id, ward_number),
                )

        yield organization
