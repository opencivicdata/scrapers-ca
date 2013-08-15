from pupa.scrape import Jurisdiction

from .people import Richmond_HillPersonScraper
from utils import lxmlize

class Richmond_Hill(Jurisdiction):
  jurisdiction_id = 'ca-on-richmond_hill'
  geographic_code = 3519038
  def get_metadata(self):
    return {
      'name': 'Richmond_Hill',
      'legislature_name': 'Richmond_Hill City Council',
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
        return Richmond_HillPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    