from pupa.scrape import Jurisdiction

from .people import WestmountPersonScraper
from utils import lxmlize

class Westmount(Jurisdiction):
  jurisdiction_id = 'ca-qc-westmount'
  geographic_code = 2466032
  def get_metadata(self):
    return {
      'name': 'Westmount',
      'legislature_name': 'Westmount City Council',
      'legislature_url': 'http://www.westmount.org/page.cfm?Section_ID=1&Menu_Item_ID=61',
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
        return WestmountPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    