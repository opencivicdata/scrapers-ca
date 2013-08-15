from pupa.scrape import Jurisdiction

from .people import BurlingtonPersonScraper
from utils import lxmlize

class Burlington(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3524002/council'
  geographic_code = 3524002
  def get_metadata(self):
    return {
      'name': 'Burlington',
      'legislature_name': 'Burlington City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
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
        return BurlingtonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    