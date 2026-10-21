from pupa.scrape import Organization

from utils import CanadianJurisdiction


class PrinceEdwardCounty(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3513020"
    division_name = "Prince Edward County"
    name = "Prince Edward County Council"
    url = "https://www.thecounty.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        wards = [
            ("Picton", 2),
            ("Bloomfield/Hallowell", 2),
            ("Wellington", 1),
            ("Ameliasburgh", 3),
            ("Athol", 1),
            ("Sophiasburgh", 1),
            ("Hillier", 1),
            ("North Marysburgh", 1),
            ("South Marysburgh", 1),
        ]
        for ward, seats in wards:
            for seat in range(1, seats + 1):
                label = f"{ward} (seat {seat})" if seats > 1 else ward
                organization.add_post(role="Councillor", label=label, division_id=self.division_id)
        yield organization
