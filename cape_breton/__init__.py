from pupa.scrape import Jurisdiction

from .people import Cape_BretonPersonScraper
from utils import lxmlize

import re

class Cape_Breton(Jurisdiction):
  jurisdiction_id = 'ca-ns-cape_breton'
  geographic_code = 1217030
  def get_metadata(self):
    return {
      'name': 'Cape Breton',
      'legislature_name': 'Cape Breton City Council',
      'legislature_url': 'http://www.cbrm.ns.ca/councillors.html',
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
        return Cape_BretonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    