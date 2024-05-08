from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Edmonton(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:4811061"
    division_name = "Edmonton"
    name = "Edmonton City Council"
    url = "http://www.edmonton.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)

        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)
        for ward_number, ward_name in enumerate(
            (
                "Anirniq",
                "Dene",
                "Ipiihkoohkanipiaohtsi",
                "Karhiio",
                "Métis",
                "Nakota Isga",
                "O-day'min",
                "papastew",
                "pihêsiwin",
                "sipiwiyiniwak",
                "Sspomitapi",
                "tastawiyiniwak",
            ),
            1,
        ):
            organization.add_post(
                role="Councillor", label=ward_name, division_id="{}/ward:{}".format(self.division_id, ward_number)
            )
        yield organization
