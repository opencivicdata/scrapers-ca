from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Guelph(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3523008"
    division_name = "Guelph"
    name = "Guelph City Council"
    url = "http://guelph.ca"
    use_type_id = True

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number in range(1, 7):
            for seat_number in range(1, 3):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
