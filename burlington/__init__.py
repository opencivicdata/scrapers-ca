from pupa.scrape import Jurisdiction

from .people import BurlingtonPersonScraper
from utils import lxmlize

import re

class Burlington(Jurisdiction):
  jurisdiction_id = 'ca-on-burlington'
  geographic_code = 3524002
  def get_metadata(self):
    return {
      'name': 'Burlington',
      'legislature_name': 'Burlington City Council',
      'legislature_url': 'http://cms.burlington.ca/Page110.aspx',
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
        return BurlingtonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    