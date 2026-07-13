from pupa.scrape import Organization

from utils import CanadianJurisdiction


class Ottawa(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/csd:3506008"
    division_name = "Ottawa"
    name = "Ottawa City Council"
    url = "http://www.ottawa.ca"

    def get_organizations(self):
        organization = Organization(self.name, classification=self.classification)
        organization.add_post(role="Mayor", label=self.division_name, division_id=self.division_id)

        wards = [
            "Orléans East-Cumberland",
            "Orléans West-Innes",
            "Barrhaven West",
            "Kanata North",
            "West Carleton-March",
            "Stittsville",
            "Bay",
            "College",
            "Knoxdale-Merivale",
            "Gloucester-Southgate",
            "Beacon Hill-Cyrville",
            "Rideau-Vanier",
            "Rideau-Rockcliffe",
            "Somerset",
            "Kitchissippi",
            "River",
            "Capital",
            "Alta Vista",
            "Orléans South-Navan",
            "Osgoode (November 15, 2022 to February 27, 2025)",
            "Osgoode (June 18, 2025 to present)",
            "Rideau-Jock",
            "Riverside South-Findlay Creek",
            "Kanata South",
            "Barrhaven East",
        ]
        for ward in wards:
            organization.add_post(role="Councillor", label=ward, division_id=self.division_id)

        yield organization
