from pupa.scrape import Jurisdiction

from .people import StratfordPersonScraper
from utils import lxmlize

import re

class Stratford(Jurisdiction):
  jurisdiction_id = 'ca-pe-stratford'
  geographic_code = 3531011
  def get_metadata(self):
    return {
      'name': 'Stratford',
      'legislature_name': 'Stratford City Council',
      'legislature_url': 'http://www.townofstratford.ca/town-hall/government/town-council/',
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
        return StratfordPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    