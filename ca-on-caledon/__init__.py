from pupa.scrape import Jurisdiction

from .people import CaledonPersonScraper
from utils import lxmlize

class Caledon(Jurisdiction):
  jurisdiction_id = 'ca-on-caledon'
  geographic_code = 3521024
  def get_metadata(self):
    return {
      'name': 'Caledon',
      'legislature_name': 'Caledon City Council',
      'legislature_url': 'http://www.town.caledon.on.ca/en/townhall/council.asp',
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
        return CaledonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    