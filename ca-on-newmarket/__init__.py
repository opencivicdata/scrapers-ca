from pupa.scrape import Jurisdiction

from .people import NewmarketPersonScraper
from utils import lxmlize

import re

class Newmarket(Jurisdiction):
  jurisdiction_id = 'ca-on-newmarket'
  geographic_code = 3519048
  def get_metadata(self):
    return {
      'name': 'Newmarket',
      'legislature_name': 'Newmarket City Council',
      'legislature_url': 'http://www.newmarket.ca/en/townhall/contactinformationmayorandtowncouncil.asp',
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
        return NewmarketPersonScraper

  def scrape_session_list(self):
    return ['2010-2014']
    