from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Mercier_Hochelaga_Maisonneuve(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-mercier-hochelaga-maisonneuve'

  def _get_metadata(self):
    return {
      'name': 'Mercier-Hochelaga-Maisonneuve',
      'legislature_name': 'Mercier-Hochelaga-Maisonneuve Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper

    