from pupa.scrape import Jurisdiction

from .people import Thunder_BayPersonScraper
from utils import lxmlize

import re

class Thunder_Bay(Jurisdiction):
  jurisdiction_id = 'ca-on-thunder_bay'
  geographic_code = 3558004
  def get_metadata(self):
    return {
      'name': 'Thunder Bay',
      'legislature_name': 'Thunder Bay City Council',
      'legislature_url': 'http://www.thunderbay.ca/City_Government/Your_Council.htm',
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
        return Thunder_BayPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    