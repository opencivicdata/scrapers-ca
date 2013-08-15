from pupa.scrape import Jurisdiction

from .people import MiltonPersonScraper
from utils import lxmlize

import re

class Milton(Jurisdiction):
  jurisdiction_id = 'ca-on-milton'
  geographic_code = 3524009
  def get_metadata(self):
    return {
      'name': 'Milton',
      'legislature_name': 'Milton City Council',
      'legislature_url': 'http://www.milton.ca/en/townhall/mayorandcouncil.asp?_mid_=5972',
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
        return MiltonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    