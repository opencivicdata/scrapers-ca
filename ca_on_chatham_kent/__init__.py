from pupa.scrape import Jurisdiction

from .people import Chatham_KentPersonScraper
from utils import lxmlize

class Chatham_Kent(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/csd:3536020/council'
  geographic_code = 3536020
  def get_metadata(self):
    return {
      'name': 'Chatham-Kent',
      'legislature_name': 'Chatham-Kent City Council',
      'legislature_url': 'http://www.chatham-kent.ca/Council/councilmembers/Pages/CouncilMembers.aspx',
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
        return Chatham_KentPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    