from pupa.scrape import Jurisdiction

from .people import Thunder_BayPersonScraper
from utils import lxmlize

class Thunder_Bay(Jurisdiction):
  jurisdiction_id = 'ca-on-thunder_bay'
  geographic_code = 3558004
  def get_metadata(self):
    return {
      'name': 'Thunder Bay',
      'legislature_name': 'Thunder Bay City Council',
      'legislature_url': 'http://www.thunderbay.ca/City_Government/Your_Council.htm',
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
        return Thunder_BayPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    