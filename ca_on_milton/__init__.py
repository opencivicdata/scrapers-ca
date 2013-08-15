from pupa.scrape import Jurisdiction

from .people import MiltonPersonScraper
from utils import lxmlize

class Milton(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3524009/council'
  geographic_code = 3524009
  def get_metadata(self):
    return {
      'name': 'Milton',
      'legislature_name': 'Milton City Council',
      'legislature_url': 'http://www.milton.ca/en/townhall/mayorandcouncil.asp?_mid_=5972',
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
        return MiltonPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    