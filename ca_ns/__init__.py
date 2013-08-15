from pupa.scrape import Jurisdiction

from .people import NovaScotiaPersonScraper
from utils import lxmlize

class NovaScotia(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:ns/legislature'
  geographic_code = 12
  def get_metadata(self):
    return {
      'name': 'Nova Scotia',
      'legislature_name': 'Nova Scotia City Council',
      'legislature_url': 'http://www.unsm.ca/doc_download/880-mayor-list-2013',
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
        return NovaScotiaPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    