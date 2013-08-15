from pupa.scrape import Jurisdiction

from .people import SaguenayPersonScraper
from utils import lxmlize

class Saguenay(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2494068/council'
  geographic_code = 2494068
  def get_metadata(self):
    return {
      'name': 'Saguenay',
      'legislature_name': 'Saguenay City Council',
      'legislature_url': 'http://ville.saguenay.ca/fr/administration-municipale/conseils-municipaux-et-darrondissement/membres-des-conseils',
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
        return SaguenayPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    