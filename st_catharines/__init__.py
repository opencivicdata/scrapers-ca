from pupa.scrape import Jurisdiction

from .people import St_CatharinesPersonScraper
from utils import lxmlize

import re

class St_Catharines(Jurisdiction):
  jurisdiction_id = 'ca-on-st_catharines'
  geographic_code = 3526053
  def get_metadata(self):
    return {
      'name': 'St. Catharines',
      'legislature_name': 'St. Catharines City Council',
      'legislature_url': 'http://www.stcatharines.ca/en/governin/BrianMcMullanMayor.asp',
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
        return St_CatharinesPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    