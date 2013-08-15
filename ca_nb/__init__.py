from pupa.scrape import Jurisdiction

from .people import NewBrunswickPersonScraper
from utils import lxmlize

class NewBrunswick(Jurisdiction):
  jurisdiction_id = 'ocd-jurisdiction/country:ca/province:nb/legislature'
  geographic_code = 13
  def get_metadata(self):
    return {
      'name': 'New Brunswick',
      'legislature_name': 'New Brunswick City Council',
      'legislature_url': 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html',
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
        return NewBrunswickPersonScraper

  def scrape_session_list(self):
    return ['N/A']
    