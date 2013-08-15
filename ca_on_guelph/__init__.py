from pupa.scrape import Jurisdiction

from .people import GuelphPersonScraper
from utils import lxmlize

class Guelph(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3523008/council'
  geographic_code = 3523008
  def get_metadata(self):
    return {
      'name': 'Guelph',
      'legislature_name': 'Guelph City Council',
      'legislature_url': 'http://guelph.ca/city-hall/mayor-and-council/city-council/',
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
        return GuelphPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    