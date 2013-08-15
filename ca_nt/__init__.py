from pupa.scrape import Jurisdiction

from .people import Northwest_TerritoriesPersonScraper
from utils import lxmlize

class Northwest_Territories(Jurisdiction):
  jurisdiction_id = 'ca-nt'
  geographic_code = 61
  def get_metadata(self):
    return {
      'name': 'Northwest Territories',
      'legislature_name': 'Northwest Territories City Council',
      'legislature_url': 'http://www.nwtac.com/about/communities/',
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
        return Northwest_TerritoriesPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    