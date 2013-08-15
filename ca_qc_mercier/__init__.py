from pupa.scrape import Jurisdiction

from .people import MercierPersonScraper
from utils import lxmlize

class Mercier(Jurisdiction):
  jurisdiction_id = 'ca-qc-mercier'
  geographic_code = 2466072
  def get_metadata(self):
    return {
      'name': 'Mercier',
      'legislature_name': 'Mercier City Council',
      'legislature_url': 'http://www.ville.mercier.qc.ca/02_viedemocratique/default.asp',
      'terms': [{
        'name': 'N/A',
        'sessions': ['N/A'],
      }],
      'provides': ['people'],
      'session_details': {
        'N/A': {
          '_scraped_name': 'N/A',
        }
      },
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return MercierPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    