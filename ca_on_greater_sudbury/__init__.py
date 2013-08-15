from pupa.scrape import Jurisdiction

from .people import GreaterSudburyPersonScraper
from utils import lxmlize

class GreaterSudbury(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3553005/council'
  geographic_code = 3553005
  def get_metadata(self):
    return {
      'name': 'Sudbury',
      'legislature_name': 'Sudbury City Council',
      'legislature_url': 'http://www.greatersudbury.ca/inside-city-hall/city-council/',
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
        return GreaterSudburyPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    