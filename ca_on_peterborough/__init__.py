from pupa.scrape import Jurisdiction

from .people import PeterboroughPersonScraper
from utils import lxmlize

class Peterborough(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3515014/council'
  geographic_code = 3515014
  def get_metadata(self):
    return {
      'name': 'Peterborough',
      'legislature_name': 'Peterborough City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
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
        return PeterboroughPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    