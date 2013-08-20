from ca_qc_montreal import MontrealPersonScraper
from utils import CanadianJurisdiction


class Ville_Marie(CanadianJurisdiction):
  jurisdiction_id = 'ca-qc-ville-marie'

  def _get_metadata(self):
    return {
      'name': 'Ville-Marie',
      'legislature_name': 'Ville-Marie Borough Council',
      'legislature_url': 'http://depot.ville.montreal.qc.ca/bd-elus/data.json',
      'provides': ['people'],
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MontrealPersonScraper
