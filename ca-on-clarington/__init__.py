from pupa.scrape import Jurisdiction

from .people import ClaringtonPersonScraper
from utils import lxmlize

import re

class Clarington(Jurisdiction):
  jurisdiction_id = 'ca-on-clarington'
  geographic_code = 3518017
  def get_metadata(self):
    return {
      'name': 'Clarington',
      'legislature_name': 'Clarington City Council',
      'legislature_url': 'http://www.clarington.net/htdocs/council_bios.html',
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
        return ClaringtonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    