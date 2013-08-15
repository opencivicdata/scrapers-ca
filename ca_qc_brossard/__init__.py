from pupa.scrape import Jurisdiction

from .people import BrossardPersonScraper
from utils import lxmlize

class Brossard(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2458007/council'
  geographic_code = 2458007
  def get_metadata(self):
    return {
      'name': 'Brossard',
      'legislature_name': 'Brossard City Council',
      'legislature_url': 'http://www.ville.brossard.qc.ca/Ma-ville/conseil-municipal.aspx?lang=en-CA',
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
        return BrossardPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    