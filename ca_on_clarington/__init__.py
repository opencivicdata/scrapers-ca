from pupa.scrape import Jurisdiction

from .people import ClaringtonPersonScraper
from utils import lxmlize

class Clarington(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3518017/council'
  geographic_code = 3518017
  def get_metadata(self):
    return {
      'name': 'Clarington',
      'legislature_name': 'Clarington City Council',
      'legislature_url': 'http://www.clarington.net/htdocs/council_bios.html',
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
        return ClaringtonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    