from pupa.scrape import Jurisdiction

from .people import MonctonPersonScraper
from utils import lxmlize

import re

class Moncton(Jurisdiction):
  jurisdiction_id = 'ca-on-moncton'
  geographic_code = 1307022
  def get_metadata(self):
    return {
      'name': 'Moncton',
      'legislature_name': 'Moncton City Council',
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
        return MonctonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    