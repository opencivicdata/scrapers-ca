from pupa.scrape import Organization

from utils import CanadianJurisdiction


class ChathamKent(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3536020"
    division_name = "Chatham-Kent"
    name = "Chatham-Kent Municipal Council"
    url = "http://www.chatham-kent.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number, stop in enumerate((3, 4, 3, 3, 3, 7), 1):
            for seat_number in range(1, stop):
                organization.add_post(
                    role="Councillor",
                    label=f"Ward {ward_number} (seat {seat_number})",
                    division_id=f"{self.division_id}/ward:{ward_number}",
                )

        yield organization
