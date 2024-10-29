from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Peel(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/cd:3521"
    division_name = "Peel"
    name = "Peel Regional Council"
    url = "http://www.peelregion.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Regional Chair", label=self.division_name, division_id=self.division_id)
        organization.add_post(role="Mayor", label="Caledon", division_id="ocd-division/country:ca/csd:3521024")
        organization.add_post(role="Mayor", label="Brampton", division_id="ocd-division/country:ca/csd:3521010")
        organization.add_post(role="Mayor", label="Mississauga", division_id="ocd-division/country:ca/csd:3521005")
        for ward_number in range(1, 7):
            organization.add_post(
                role="Councillor",
                label=f"Caledon Ward {ward_number} (seat 1)",
                division_id=f"ocd-division/country:ca/csd:3521024/ward:{ward_number}",
            )
        for ward_number in range(1, 11):
            for seat_number in range(1, 3 if ward_number <= 6 else 2):
                organization.add_post(
                    role="Councillor",
                    label=f"Brampton Ward {ward_number} (seat {seat_number})",
                    division_id=f"ocd-division/country:ca/csd:3521010/ward:{ward_number}",
                )
        for ward_number in range(1, 12):
            organization.add_post(
                role="Councillor",
                label=f"Mississauga Ward {ward_number} (seat 1)",
                division_id=f"ocd-division/country:ca/csd:3521005/ward:{ward_number}",
            )

        yield organization
