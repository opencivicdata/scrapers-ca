from pupa.scrape import Jurisdiction

from .people import CaledonPersonScraper
from utils import lxmlize

import re

class Caledon(Jurisdiction):
  jurisdiction_id = 'ca-on-caledon'
  geographic_code = 3521024
  def get_metadata(self):
    return {
      'name': 'Caledon',
      'legislature_name': 'Caledon City Council',
      'legislature_url': 'http://www.town.caledon.on.ca/en/townhall/council.asp',
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
        return CaledonPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    