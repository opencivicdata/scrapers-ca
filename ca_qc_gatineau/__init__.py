from pupa.scrape import Jurisdiction

from .people import GatineauPersonScraper
from utils import lxmlize

class Gatineau(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:2481017/council'
  geographic_code = 2481017
  def get_metadata(self):
    return {
      'name': 'Gatineau',
      'legislature_name': 'Gatineau Municipal Council',
      'legislature_url': 'http://www.gatineau.ca/page.asp?p=la_ville/conseil_municipal',
      'terms': [{
        'name': '2009-2013',
        'sessions': ['2009-2013'],
        'start_year': 2009,
        'end_year': 2013,
      }],
      'provides': ['people'],
      'session_details': {
        '2009-2013': {
          '_scraped_name': '2009-2013',
        }
      },
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return GatineauPersonScraper

  def scrape_session_list(self):
    return ['2009-2013']
    