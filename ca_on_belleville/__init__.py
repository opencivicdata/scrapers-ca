from pupa.scrape import Jurisdiction

from .people import BellevillePersonScraper
from utils import lxmlize

class Belleville(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3512005/council'
  geographic_code = 3512005
  def get_metadata(self):
    return {
      'name': 'Belleville',
      'legislature_name': 'Belleville City Council',
      'legislature_url': 'http://www.city.belleville.on.ca/CITYHALL/MAYORANDCOUNCIL/Pages/CityCouncil.aspx',
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
        return BellevillePersonScraper

  def scrape_session_list(self):
    return ['N/A']
    