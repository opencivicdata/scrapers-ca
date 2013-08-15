from pupa.scrape import Jurisdiction

from .people import LaSallePersonScraper
from utils import lxmlize

class LaSalle(Jurisdiction):
  jurisdiction_id = 'ca-qc-lasalle'

  def get_metadata(self):
    return {
      'name': 'LaSalle',
      'legislature_name': 'LaSalle City Council',
      'legislature_url': 'http://www.town.lasalle.on.ca/Council/council-council.htm',
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
        return LaSallePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    