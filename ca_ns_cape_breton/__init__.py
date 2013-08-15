from pupa.scrape import Jurisdiction

from .people import Cape_BretonPersonScraper
from utils import lxmlize

class Cape_Breton(Jurisdiction):
  jurisdiction_id = 'ca-ns-cape_breton'
  geographic_code = 1217030
  def get_metadata(self):
    return {
      'name': 'Cape Breton',
      'legislature_name': 'Cape Breton City Council',
      'legislature_url': 'http://www.cbrm.ns.ca/councillors.html',
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
        return Cape_BretonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    