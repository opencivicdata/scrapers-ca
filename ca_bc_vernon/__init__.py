from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Vernon(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:5937014"
    division_name = "Vernon"
    name = "Vernon City Council"
    url = "https://www.vernon.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label="Vernon", division_id=self.division_id)
        for i in range(1, 7):
            organization.add_post(role="Councillor", label=f"Vernon (seat {i})", division_id=self.division_id)
        yield organization
