from pupa.scrape import Jurisdiction

from .people import Nova_ScotiaPersonScraper
from utils import lxmlize

import re

class Nova_Scotia(Jurisdiction):
  jurisdiction_id = 'ca-ns'
  geographic_code = 12
  def get_metadata(self):
    return {
      'name': 'Nova Scotia',
      'legislature_name': 'Nova Scotia City Council',
      'legislature_url': 'http://www.unsm.ca/doc_download/880-mayor-list-2013',
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
        return Nova_ScotiaPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    