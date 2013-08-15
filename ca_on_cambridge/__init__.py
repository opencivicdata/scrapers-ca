from pupa.scrape import Jurisdiction

from .people import CambridgePersonScraper
from utils import lxmlize

class Cambridge(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3530010/council'
  geographic_code = 3530010
  def get_metadata(self):
    return {
      'name': 'Cambridge',
      'legislature_name': 'Cambridge City Council',
      'legislature_url': 'http://www.cambridge.ca/cs_mayor/wards_councillors.php?cpid=51&sid=57',
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
        return CambridgePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    