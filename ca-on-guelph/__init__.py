from pupa.scrape import Jurisdiction

from .people import GuelphPersonScraper
from utils import lxmlize

import re

class Guelph(Jurisdiction):
  jurisdiction_id = 'ca-on-guelph'
  geographic_code = 3523008
  def get_metadata(self):
    return {
      'name': 'Guelph',
      'legislature_name': 'Guelph City Council',
      'legislature_url': 'http://guelph.ca/city-hall/mayor-and-council/city-council/',
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
        return GuelphPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    