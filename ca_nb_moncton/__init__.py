from pupa.scrape import Jurisdiction

from .people import MonctonPersonScraper
from utils import lxmlize

class Moncton(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:1307022/council'
  geographic_code = 1307022
  def get_metadata(self):
    return {
      'name': 'Moncton',
      'legislature_name': 'Moncton City Council',
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
        return MonctonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    