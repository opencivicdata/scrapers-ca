from pupa.scrape import Jurisdiction

from .people import KirklandPersonScraper
from utils import lxmlize

import re

class Kirkland(Jurisdiction):
  jurisdiction_id = 'ca-qc-kirkland'
  geographic_code = 2466102
  def get_metadata(self):
    return {
      'name': 'Kirkland',
      'legislature_name': 'Kirkland City Council',
      'legislature_url': 'http://www.ville.kirkland.qc.ca/portrait-municipal/conseil-municipal/elus-municipaux',
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
        return KirklandPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    