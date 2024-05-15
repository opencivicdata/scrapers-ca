from utils import CanadianJurisdiction


class CanadaMunicipalities(CanadianJurisdiction):
    classification = "legislature"
    division_id = "ocd-division/country:ca"
    division_name = "Canada"
    name = "Canada rural towns and villages municipal councils"
    url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrGXQy8qk16OhuTjlccoGB4jL5e8X1CEqRbg896ufLdh67DQk9nuGm-oufIT0HRMPEnwePw2HDx1Vj/pub?gid=0&single=true&output=csv"

    def get_organizations(self):
        return []
