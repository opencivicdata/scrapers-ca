from pupa.scrape import Organization

from utils import CanadianJurisdiction


class GrandePrairieCountyNo1(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4819006"
    division_name = "Grande Prairie County No. 1"
    name = "County of Grande Prairie No. 1 Council"
    url = "http://www.countygp.ab.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        for division_number in range(1, 10):
            # One of the councillors is the Reeve.
            if division_number == 5:
                role = "Reeve"
            # One of the councillors is the Deputy Reeve
            elif division_number == 7:
                role = "Deputy Reeve"
            else:
                role = "Councillor"
            organization.add_post(
                role=role,
                label="Division {}".format(division_number),
                division_id="{}/division:{}".format(self.division_id, division_number),
            )

        yield organization
