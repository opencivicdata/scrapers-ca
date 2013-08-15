from pupa.scrape import Jurisdiction

from .people import Wood_BuffaloPersonScraper
from utils import lxmlize

class Wood_Buffalo(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:4816037/council'
  geographic_code = 4816037
  def get_metadata(self):
    return {
      'name': 'Wood Buffalo',
      'legislature_name': 'Wood Buffalo City Council',
      'legislature_url': 'http://www.woodbuffalo.ab.ca/Municipal-Government/Mayor-and-Council/Councillor-Profiles.htm',
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
        return Wood_BuffaloPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    