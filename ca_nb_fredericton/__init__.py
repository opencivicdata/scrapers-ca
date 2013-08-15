from pupa.scrape import Jurisdiction

from .people import FrederictonPersonScraper
from utils import lxmlize

class Fredericton(Jurisdiction):
  jurisdiction_id = 'ca-nb-fredericton'
  geographic_code = 1310032
  def get_metadata(self):
    return {
      'name': 'Fredericton',
      'legislature_name': 'Fredericton City Council',
      'legislature_url': 'http://www.fredericton.ca/en/citygovernment/CityCouncil.asp',
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
        return FrederictonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    