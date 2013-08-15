from pupa.scrape import Jurisdiction

from .people import RichmondHillPersonScraper
from utils import lxmlize

class RichmondHill(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3519038/council'
  geographic_code = 3519038
  def get_metadata(self):
    return {
      'name': 'Richmond Hill',
      'legislature_name': 'Richmond Hill City Council',
      'legislature_url': 'http://www.richmondhill.ca/subpage.asp?pageid=townhall_members_of_the_council',
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
        return RichmondHillPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    