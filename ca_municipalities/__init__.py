from pupa.scrape.base import BaseModel
from utils import CanadianJurisdiction


class CanadaMunicipalities(CanadianJurisdiction):
    classification = 'upper'
    division_id = 'ocd-division/country:ca'
    division_name = 'Canada'
    name = 'Canada rural towns and villages municipal councils'
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQzUYBs5WnnMaFtdu6l98jPsJpTXR-mJqdRG6Beb02JMSmvq6FgZCGraBEUESuhEzNX8TDhqX2p1YM8/pub?output=csv'
    #url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vRrGXQy8qk16OhuTjlccoGB4jL5e8X1CEqRbg896ufLdh67DQk9nuGm-oufIT0HRMPEnwePw2HDx1Vj/pub?output=csv'

    def get_organizations(self):
        return []