from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Waterloo(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/cd:3530"
    division_name = "Waterloo"
    name = "Waterloo Regional Council"
    url = "http://www.regionofwaterloo.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Chair", label=self.division_name, division_id=self.division_id)
        organization.add_post(
            role="Regional Councillor", label="North Dumfries", division_id="ocd-division/country:ca/csd:3530004"
        )
        organization.add_post(
            role="Regional Councillor", label="Wellesley", division_id="ocd-division/country:ca/csd:3530027"
        )
        organization.add_post(
            role="Regional Councillor", label="Wilmot", division_id="ocd-division/country:ca/csd:3530020"
        )
        organization.add_post(
            role="Regional Councillor", label="Woolwich", division_id="ocd-division/country:ca/csd:3530035"
        )
        for seat_number in range(1, 4):
            organization.add_post(
                role="Regional Councillor",
                label=f"Cambridge (seat {seat_number})",
                division_id="ocd-division/country:ca/csd:3530010",
            )
        for seat_number in range(1, 6):
            organization.add_post(
                role="Regional Councillor",
                label=f"Kitchener (seat {seat_number})",
                division_id="ocd-division/country:ca/csd:3530013",
            )
        for seat_number in range(1, 4):
            organization.add_post(
                role="Regional Councillor",
                label=f"Waterloo (seat {seat_number})",
                division_id="ocd-division/country:ca/csd:3530016",
            )

        yield organization
