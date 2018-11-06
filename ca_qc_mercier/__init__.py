from utils import CanadianJurisdiction
from pupa.scrape import Organization


class Mercier(CanadianJurisdiction):
    classification = 'legislature'
    division_id = 'ocd-division/country:ca/csd:2467045'
    division_name = 'Mercier'
    name = 'Conseil municipal de Mercier'
    url = 'http://www.ville.mercier.qc.ca'
