from pupa.scrape import Jurisdiction

from .people import NewmarketPersonScraper
from utils import lxmlize

class Newmarket(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519048/council'
  geographic_code = 3519048
  def get_metadata(self):
    return {
      'name': 'Newmarket',
      'legislature_name': 'Newmarket City Council',
      'legislature_url': 'http://www.newmarket.ca/en/townhall/contactinformationmayorandtowncouncil.asp',
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
        return NewmarketPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    