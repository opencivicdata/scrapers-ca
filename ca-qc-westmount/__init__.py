from pupa.scrape import Jurisdiction

from .people import WestmountPersonScraper
from utils import lxmlize

import re

class Westmount(Jurisdiction):
  jurisdiction_id = 'ca-qc-westmount'
  geographic_code = 2466032
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
    }

  def get_scraper(self, term, session, scraper_type):
    if scraper_type == 'people':
        return WestmountPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    