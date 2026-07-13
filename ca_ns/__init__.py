from pupa.scrape import Organization

from utils import CanadianJurisdiction


class NovaScotia(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca/province:ns"
    division_name = "Nova Scotia"
    name = "Nova Scotia House of Assembly"
    url = "http://nslegislature.ca"
    parties = [
        {"name": "Nova Scotia Liberal Party"},
        {"name": "Progressive Conservative Association of Nova Scotia"},
        {"name": "Nova Scotia New Democratic Party"},
        {"name": "Independent"},
    ]

    def get_organizations(self):
        for item in super().get_organizations():
            if isinstance(item, Organization):
                item.add_post(
                    role="MLA",
                    label="Ch\u00e9ticamp-Margarees-Pleasant Bay",
                    division_id=self.division_id,
                )
            yield item
