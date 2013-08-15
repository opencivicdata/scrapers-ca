from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction

class Riviere_des_Prairies_Pointe_aux_Trembles(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-riviere-des-prairies-pointe-aux-trembles'

  def _get_metadata(self):
    return {
      'name': 'Riviere-des-Prairies-Pointe-aux-Trembles',
      'legislature_name': 'Riviere-des-Prairies-Pointe-aux-Trembles Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
