from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Ahuntsic_Cartierville(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-ahuntsic-cartierville'

  def _get_metadata(self):
    return {
      'name': 'Ahuntsic-Cartierville',
      'legislature_name': 'Ahuntsic-Cartierville Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
