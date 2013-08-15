from pupa.scrape import Jurisdiction

from .people import KirklandPersonScraper
from utils import lxmlize

class Kirkland(Jurisdiction):
  jurisdiction_id = 'ca-qc-kirkland'
  geographic_code = 2466102
  def get_metadata(self):
    return {
      'name': 'Kirkland',
      'legislature_name': 'Kirkland City Council',
      'legislature_url': 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux',
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
        return KirklandPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    