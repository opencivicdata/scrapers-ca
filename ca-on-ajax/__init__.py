from pupa.scrape import Jurisdiction

from .people import AjaxPersonScraper
from utils import lxmlize

import re

class Ajax(Jurisdiction):
  jurisdiction_id = 'ca-on-ajax'
  geographic_code = 3518005
  def get_metadata(self):
    return {
      'name': 'Ajax',
      'legislature_name': 'Ajax City Council',
      'legislature_url': 'http://www.ajax.ca/en/insidetownhall/mayorcouncillors.asp',
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
        return AjaxPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    