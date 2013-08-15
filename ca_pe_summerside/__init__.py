from pupa.scrape import Jurisdiction

from .people import SummersidePersonScraper
from utils import lxmlize

class Summerside(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:1103025/council'
  geographic_code = 1103025
  def get_metadata(self):
    return {
      'name': 'Summerside',
      'legislature_name': 'Summerside City Council',
      'legislature_url': 'http://city.summerside.pe.ca/mayor-and-council/pages/2012/2/councillors/',
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
        return SummersidePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    