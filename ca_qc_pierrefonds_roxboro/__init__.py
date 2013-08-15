from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Pierrefonds_Roxboro(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-pierrefonds-roxboro'

  def _get_metadata(self):
    return {
      'name': 'Pierrefonds-Roxboro',
      'legislature_name': 'Pierrefonds-Roxboro Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper

    