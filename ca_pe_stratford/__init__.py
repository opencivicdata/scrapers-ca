from pupa.scrape import Jurisdiction

from .people import StratfordPersonScraper
from utils import lxmlize

class Stratford(Jurisdiction):
  jurisdiction_id = 'ca-pe-stratford'
  geographic_code = 3531011
  def get_metadata(self):
    return {
      'name': 'Stratford',
      'legislature_name': 'Stratford City Council',
      'legislature_url': 'http://www.townofstratford.ca/town-hall/government/town-council/',
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
        return StratfordPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    