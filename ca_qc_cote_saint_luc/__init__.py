from pupa.scrape import Jurisdiction

from .people import Cote_St_LucPersonScraper
from utils import lxmlize

class Cote_St_Luc(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2466058/council'
  geographic_code = 2466058
  def get_metadata(self):
    return {
      'name': 'Cote_St-Luc',
      'legislature_name': 'Cote St-Luc City Council',
      'legislature_url': 'http://www.cotesaintluc.org/Administration',
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
        return Cote_St_LucPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    