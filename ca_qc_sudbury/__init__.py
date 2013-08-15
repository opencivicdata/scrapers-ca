from pupa.scrape import Jurisdiction

from .people import SudburyPersonScraper
from utils import lxmlize

class Gatineau(Jurisdiction):
  jurisdiction_id = 'ca-qc-sudbury'
  geographic_code = 3553005
  def get_metadata(self):
    return {
      'name': 'Sudbury',
      'legislature_name': 'Sudbury City Council',
      'legislature_url': 'http://www.greatersudbury.ca/inside-city-hall/city-council/',
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
        return SudburyPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    