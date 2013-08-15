from pupa.scrape import Jurisdiction

from .people import SennevillePersonScraper
from utils import lxmlize

class Senneville(Jurisdiction):
  jurisdiction_id = 'ca-qc-senneville'
  geographic_code = 2466127
  def get_metadata(self):
    return {
      'name': 'Senneville',
      'legislature_name': 'Senneville City Council',
      'legislature_url': 'http://www.villagesenneville.qc.ca/fr/membres-du-conseil-municipal',
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
        return SennevillePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    