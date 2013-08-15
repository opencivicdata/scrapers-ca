from pupa.scrape import Jurisdiction

from .people import New_BrunswickPersonScraper
from utils import lxmlize

import re

class New_Brunswick(Jurisdiction):
  jurisdiction_id = 'ca-nb'
  geographic_code = 13
  def get_metadata(self):
    return {
      'name': 'New Brunswick',
      'legislature_name': 'New Brunswick City Council',
      'legislature_url': 'http://www2.gnb.ca/content/gnb/en/departments/elg/local_government/content/community_profiles.html',
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
        return New_BrunswickPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    