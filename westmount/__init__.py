from pupa.scrape import Jurisdiction

# from .events import TorontoEventScraper
from .people import WestmountPersonScraper
# from .votes import TorontoVoteScraper
from utils import lxmlize

import re

class Westmount(Jurisdiction):
  jurisdiction_id = 'ca-qc-westmount'

  def get_metadata(self):
    return {
      'name': 'Westmount',
      'legislature_name': 'Westmount City Council',
      'legislature_url': 'http://www.westmount.org/page.cfm?Section_ID=1&Menu_Item_ID=61',
      'terms': [{
        'name': '2010-2014',
        'sessions': ['2010-2014'],
        'start_year': 2010,
        'end_year': 2014,
      }],
      'provides': ['people'],
      'parties': [],
      'session_details': {
        '2010-2014': {
          '_scraped_name': '2010-2014',
        }
      },
      'feature_flags': [],
      # '_ignored_scraped_sessions': ['2006-2010'],
    }

  def get_scraper(self, term, session, scraper_type):
    # if scraper_type == 'events':
    #     return TorontoEventScraper
    if scraper_type == 'people':
        return WestmountPersonScraper
    # if scraper_type == 'votes':
    #     return TorontoVoteScraper

  def scrape_session_list(self):
    return ['2010-2014']
    